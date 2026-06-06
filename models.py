from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


# ==========================
# VENDOR MODEL
# ==========================
class Vendor(db.Model):

    __tablename__ = "vendors"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    vendor_name = db.Column(
        db.String(150),
        nullable=False
    )

    email = db.Column(
        db.String(120)
    )

    phone = db.Column(
        db.String(20)
    )

    gst_number = db.Column(
        db.String(20)
    )

    category = db.Column(
        db.String(100)
    )

    address = db.Column(
        db.Text
    )

    rating = db.Column(
        db.Float,
        default=0
    )

    status = db.Column(
        db.String(20),
        default="Active"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


# ==========================
# RFQ MODEL
# ==========================
class RFQ(db.Model):

    __tablename__ = "rfqs"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    description = db.Column(
        db.Text
    )

    quantity = db.Column(
        db.Integer,
        nullable=False
    )

    deadline = db.Column(
        db.String(50)
    )

    vendor_id = db.Column(
        db.Integer,
        db.ForeignKey('vendors.id')
    )

    status = db.Column(
        db.String(20),
        default="Open"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )