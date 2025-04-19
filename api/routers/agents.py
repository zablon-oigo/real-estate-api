from fastapi import APIRouter, status, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from fastapi.responses import Response
from cloudinary.uploader import upload
from typing import List
from .. import schema, utils, sql_query, models, jwt_auth
from ..database import get_db

router = APIRouter(
    prefix="/api/v1/agent",
    tags=["Agent Information"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_agent_detail(
    agent: schema.AgentBase,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(jwt_auth.get_authenticated_user)  
):
    user_agent = db.query(models.AgentDetails).filter(models.AgentDetails.user_id == current_user.id).first()
    if user_agent:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="User already has agent details")
    
    new_agent = models.AgentDetails(user_id=current_user.id, **agent.dict())
    db.add(new_agent)
    db.commit()
    db.refresh(new_agent)
    return new_agent



@router.post("/upload_agent_profile_photo", status_code=status.HTTP_200_OK)
async def upload_profile_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: int = Depends(jwt_auth.get_authenticated_user)
):
    agent_qs = db.query(models.AgentDetails).filter(models.AgentDetails.user_id == current_user.id)
    agent = agent_qs.first()
    if not agent:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    result = upload(file.file, public_id="agent_profile")
    image_url = result.get("url")
    print(image_url)

    agent_qs.update({"profile_img": image_url}, synchronize_session=False)
    db.commit()
    return agent_qs.first()

@router.get("/{agent_id}", status_code=status.HTTP_200_OK, response_model=schema.Agent)
async def get_agent_detail(agent_id: int, db: Session = Depends(get_db)):
    agent = db.query(models.AgentDetails).filter(models.AgentDetails.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    return agent

@router.patch("/{agent_id}", status_code=status.HTTP_200_OK, response_model=schema.Agent)
async def update_agent_details(
    agent_id: int,
    update_data: schema.AgentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(jwt_auth.get_authenticated_user)
):
    agent_qs = db.query(models.AgentDetails).filter(
        models.AgentDetails.id == agent_id,
        models.AgentDetails.user_id == current_user.id
    )

    agent = agent_qs.first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found or not authorized")

    agent_qs.update(update_data.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return agent_qs.first()

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schema.Agent])
async def get_agent_list(db: Session = Depends(get_db)):
    agents = sql_query.get_all_agents(db=db)
    return agents
