from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ==========================
# USER
# ==========================

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

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
        db.String(20),
        default="Manager"
    )

# ==========================
# VENDOR
# ==========================
class Vendor(db.Model):

    __tablename__ = "vendors"

    id = db.Column(db.Integer, primary_key=True)

    vendor_name = db.Column(db.String(150), nullable=False)

    email = db.Column(db.String(120))

    phone = db.Column(db.String(20))

    gst_number = db.Column(db.String(20))

    category = db.Column(db.String(100))

    address = db.Column(db.Text)

    rating = db.Column(db.Float, default=0)

    status = db.Column(db.String(20), default="Active")

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    rfqs = db.relationship(
        "RFQ",
        backref="vendor",
        lazy=True
    )

    quotations = db.relationship(
        "Quotation",
        backref="vendor",
        lazy=True
    )


# ==========================
# RFQ
# ==========================
class RFQ(db.Model):

    __tablename__ = "rfqs"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)

    description = db.Column(db.Text)

    quantity = db.Column(db.Integer)

    deadline = db.Column(db.String(50))

    vendor_id = db.Column(
        db.Integer,
        db.ForeignKey("vendors.id")
    )

    status = db.Column(
        db.String(20),
        default="Open"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    quotations = db.relationship(
        "Quotation",
        backref="rfq",
        lazy=True
    )


# ==========================
# QUOTATION
# ==========================
class Quotation(db.Model):

    __tablename__ = "quotations"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

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
        db.Integer
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

    approvals = db.relationship(
        "Approval",
        backref="quotation",
        lazy=True
    )


# ==========================
# APPROVAL
# ==========================
class Approval(db.Model):

    __tablename__ = "approvals"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    quotation_id = db.Column(
        db.Integer,
        db.ForeignKey("quotations.id")
    )

    status = db.Column(
        db.String(20),
        default="Pending"
    )

    remarks = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    purchase_orders = db.relationship(
        "PurchaseOrder",
        backref="approval",
        lazy=True
    )


# ==========================
# PURCHASE ORDER
# ==========================
class PurchaseOrder(db.Model):

    __tablename__ = "purchase_orders"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    po_number = db.Column(
        db.String(50),
        unique=True
    )

    approval_id = db.Column(
        db.Integer,
        db.ForeignKey("approvals.id")
    )

    amount = db.Column(
        db.Float,
        default=0
    )

    status = db.Column(
        db.String(20),
        default="Generated"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    invoices = db.relationship(
        "Invoice",
        backref="purchase_order",
        lazy=True
    )


# ==========================
# INVOICE
# ==========================
class Invoice(db.Model):

    __tablename__ = "invoices"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    invoice_number = db.Column(
        db.String(50),
        unique=True
    )

    po_id = db.Column(
        db.Integer,
        db.ForeignKey("purchase_orders.id")
    )

    amount = db.Column(
        db.Float,
        default=0
    )

    status = db.Column(
        db.String(20),
        default="Generated"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )