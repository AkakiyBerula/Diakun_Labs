from flask import Flask, render_template, url_for, flash, redirect, request
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, ValidationError 
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
import json
import email_validator

SECRET_KEY = "vladsecretkey"
WTF_CSRF_ENABLED = True







