from fastapi import APIRouter, status, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import Response
from jose import JWTError

from .. import schema, utils, sql_query, models, jwt_auth
from ..database import get_db

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["User Authentication"]
)


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def register_user(user: schema.UserCreate, background_task: BackgroundTasks, db: Session = Depends(get_db)):
    if sql_query.check_user_exist(db, email=user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exists")

    user.password = utils.hash_password(user.password)
    user = sql_query.insert_new_user(db, user=user)

    otp_code = utils.generate_otp_code()
    otp_data = schema.OTPData(code=otp_code, user_id=user.id)

    message = f"""
    <html>
        <body>
            <h2>Hello {user.email},</h2>
            <p>Thank you for signing up. Please use the following OTP code to verify your email address:</p>
            <h3 style="color: #2F855A;">{otp_code}</h3>
            <p>This code will expire in 2 minutes.</p>
            <br/>
            <p>If you didn't sign up for this account, please ignore this email.</p>
        </body>
    </html>
    """

    utils.send_mail(background_task, subject="Email Verification", recipient=[user.email], message=message)
    sql_query.create_otp_for_user(db, otp=otp_data)

    return {
        "message": "Account created successfully. Please verify your email with the OTP sent to your inbox."
    }


@router.post("/email-verification", status_code=status.HTTP_200_OK)
async def verify_email(otp: schema.OneTimePassword, db: Session = Depends(get_db)):
    otp_user_qs = db.query(models.UserOneTimePassword).filter(models.UserOneTimePassword.code == otp.code)
    otp_user = otp_user_qs.first()

    if not otp_user:
        raise HTTPException(status_code=404, detail="Invalid OTP code")

    is_valid = utils.verify_otp(otp.code)
    if not is_valid:
        otp_user_qs.update({"is_valid": False}, synchronize_session=False)
        db.commit()
        raise HTTPException(status_code=400, detail="OTP has expired or is invalid")

    user = db.query(models.User).filter(models.User.id == otp_user.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_verified = True
    otp_user_qs.update({"is_valid": False}, synchronize_session="fetch")
    db.commit()

    return {
        "message": "Email verified successfully. You can now log in.",
        "is_verified": user.is_verified
    }


@router.post('/login', status_code=status.HTTP_200_OK)
async def jwt_token_authentication(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = sql_query.check_user_exist(db, email=credentials.username)
    if not user or not utils.verify_password(credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    access_token = jwt_auth.create_access_token(data={"user_id": user.id})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/forget-password", status_code=status.HTTP_200_OK)
async def reset_password_request(req: schema.ForgetPassword, background_task: BackgroundTasks, db: Session = Depends(get_db)):
    user = sql_query.check_user_exist(db, email=req.email)
    if not user:
        return Response(content="An email to reset your password has been sent", status_code=status.HTTP_200_OK)

    token = jwt_auth.create_access_token(data={"user_id": user.id})
    subject = "Password Reset Request"
    recipient = [user.email]
    message = f"""
    <html>
        <body>
            <p>Hello {user.email},</p>
            <p>Click the link below to reset your password:</p>
            <a href="http://127.0.0.1:8000/reset-password?token={token}">Reset Password</a>
        </body>
    </html>
    """

    utils.send_mail(background_task, subject, recipient, message)
    return {
        "message": "Email to reset your password has been sent"
    }


@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(reqBody: schema.ResetPassword, db: Session = Depends(get_db)):
    try:
        response = jwt_auth.decode_general_token(reqBody.token)
        user_qs = db.query(models.User).filter(models.User.id == response.user_id)

        if not user_qs.first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")

        hashed_pw = utils.hash_password(reqBody.password)
        user_qs.update({"password": hashed_pw}, synchronize_session=False)
        db.commit()

        return {"message": "Password reset successfully"}

    except JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token is invalid or has expired")





