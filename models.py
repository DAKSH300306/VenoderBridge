from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


# ==================================
# USER MODEL
# ==================================
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(50),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


# ==================================
# VENDOR MODEL
# ==================================
class Vendor(db.Model):
    __tablename__ = "vendors"

    id = db.Column(db.Integer, primary_key=True)

    vendor_name = db.Column(
        db.String(150),
        nullable=False
    )

    email = db.Column(db.String(120))

    phone = db.Column(db.String(20))

    gst_number = db.Column(db.String(20))

    category = db.Column(db.String(100))

    address = db.Column(db.Text)

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


# ==================================
# RFQ MODEL
# ==================================
class RFQ(db.Model):
    __tablename__ = "rfqs"

    id = db.Column(db.Integer, primary_key=True)

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
        db.Date
    )

    status = db.Column(
        db.String(20),
        default="Open"
    )

    created_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


# ==================================
# QUOTATION MODEL
# ==================================
class Quotation(db.Model):
    __tablename__ = "quotations"

    id = db.Column(db.Integer, primary_key=True)

    rfq_id = db.Column(
        db.Integer,
        db.ForeignKey("rfqs.id")
    )

    vendor_id = db.Column(
        db.Integer,
        db.ForeignKey("vendors.id")
    )

    quoted_price = db.Column(
        db.Float,
        nullable=False
    )

    delivery_days = db.Column(
        db.Integer,
        nullable=False
    )

    remarks = db.Column(
        db.Text
    )

    status = db.Column(
        db.String(20),
        default="Submitted"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


# ==================================
# APPROVAL MODEL
# ==================================
class Approval(db.Model):
    __tablename__ = "approvals"

    id = db.Column(db.Integer, primary_key=True)

    quotation_id = db.Column(
        db.Integer,
        db.ForeignKey("quotations.id")
    )

    approved_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    remarks = db.Column(
        db.Text
    )

    status = db.Column(
        db.String(20),
        default="Pending"
    )

    approval_date = db.Column(
        db.DateTime
    )


# ==================================
# PURCHASE ORDER MODEL
# ==================================
class PurchaseOrder(db.Model):
    __tablename__ = "purchase_orders"

    id = db.Column(db.Integer, primary_key=True)

    po_number = db.Column(
        db.String(50),
        unique=True
    )

    quotation_id = db.Column(
        db.Integer,
        db.ForeignKey("quotations.id")
    )

    total_amount = db.Column(
        db.Float,
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="Generated"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


# ==================================
# INVOICE MODEL
# ==================================
class Invoice(db.Model):
    __tablename__ = "invoices"

    id = db.Column(db.Integer, primary_key=True)

    invoice_number = db.Column(
        db.String(50),
        unique=True
    )

    po_id = db.Column(
        db.Integer,
        db.ForeignKey("purchase_orders.id")
    )

    subtotal = db.Column(
        db.Float,
        nullable=False
    )

    tax = db.Column(
        db.Float,
        default=18
    )

    grand_total = db.Column(
        db.Float,
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="Generated"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )