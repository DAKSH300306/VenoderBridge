from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    flash,
    send_file
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
from io import BytesIO
from reportlab.pdfgen import canvas 
from models import *

app = Flask(__name__)

# ===================================
# CONFIG
# ===================================
app.config['SECRET_KEY'] = 'vendorbridge_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vendorbridge.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':

        hashed_password = generate_password_hash(
            request.form['password']
        )

        user = User(
            name=request.form['name'],
            email=request.form['email'],
            password=hashed_password,
            role=request.form['role']
        )

        db.session.add(user)
        db.session.commit()

        return redirect('/login')

    return render_template('auth/signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        print("EMAIL:", request.form['email'])

        user = User.query.filter_by(
            email=request.form['email']
        ).first()

        print("USER:", user)

        if user:
            print(
                "PASSWORD MATCH:",
                check_password_hash(
                    user.password,
                    request.form['password']
                )
            )

        if user and check_password_hash(
            user.password,
            request.form['password']
        ):

            print("LOGIN SUCCESS")

            session['user_id'] = user.id
            session['user_name'] = user.name
            session['role'] = user.role

            return redirect('/')

        print("LOGIN FAILED")

        flash("Invalid Credentials")

    return render_template('auth/login.html')

@app.route('/logout')
def logout():

    session.clear()

    return redirect('/login')

# ===================================
# DASHBOARD
# ===================================
@app.route('/')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    
    total_vendors = Vendor.query.count()

    total_rfqs = RFQ.query.count()

    total_quotations = Quotation.query.count()

    total_approvals = Approval.query.count()

    total_purchase_orders = PurchaseOrder.query.count()

    total_invoices = Invoice.query.count()

    return render_template(
        'dashboard.html',
        total_vendors=total_vendors,
        total_rfqs=total_rfqs,
        total_quotations=total_quotations,
        total_approvals=total_approvals,
        total_purchase_orders=total_purchase_orders,
        total_invoices=total_invoices
    )
# ===================================
# VENDORS
# ===================================
@app.route('/vendors')
def vendors():
    if 'user_id' not in session:
        return redirect('/login')

    vendor_list = Vendor.query.all()

    return render_template(
        'vendors/vendor_list.html',
        vendors=vendor_list
    )


@app.route('/add_vendor', methods=['GET', 'POST'])
def add_vendor():

    if request.method == 'POST':

        vendor = Vendor(
            vendor_name=request.form['vendor_name'],
            email=request.form['email'],
            phone=request.form['phone'],
            gst_number=request.form['gst_number'],
            category=request.form['category']
        )

        db.session.add(vendor)
        db.session.commit()

        return redirect('/vendors')

    return render_template(
        'vendors/add_vendor.html'
    )


@app.route('/delete_vendor/<int:id>')
def delete_vendor(id):

    vendor = Vendor.query.get_or_404(id)

    db.session.delete(vendor)

    db.session.commit()

    return redirect('/vendors')

# ===================================
# RFQ
# ===================================
@app.route('/rfqs')
def rfqs():
    if 'user_id' not in session:
        return redirect('/login')

    rfq_list = RFQ.query.all()

    return render_template(
        'rfq/rfq_list.html',
        rfqs=rfq_list
    )


@app.route('/create_rfq', methods=['GET', 'POST'])
def create_rfq():

    vendors = Vendor.query.all()

    if request.method == 'POST':

        rfq = RFQ(
            title=request.form['title'],
            description=request.form['description'],
            quantity=request.form['quantity'],
            deadline=request.form['deadline'],
            vendor_id=request.form['vendor_id']
        )

        db.session.add(rfq)
        db.session.commit()

        return redirect('/rfqs')

    return render_template(
        'rfq/create_rfq.html',
        vendors=vendors
    )

# ===================================
# QUOTATIONS
# ===================================
@app.route('/quotations')
def quotations():
    if 'user_id' not in session:
        return redirect('/login')

    quotation_list = Quotation.query.all()

    return render_template(
        'quotations/quotation_list.html',
        quotations=quotation_list
    )


@app.route('/add_quotation', methods=['GET', 'POST'])
def add_quotation():

    rfqs = RFQ.query.all()
    vendors = Vendor.query.all()

    if request.method == 'POST':

        quotation = Quotation(
            rfq_id=request.form['rfq_id'],
            vendor_id=request.form['vendor_id'],
            quoted_price=request.form['quoted_price'],
            delivery_days=request.form['delivery_days'],
            remarks=request.form['remarks']
        )

        db.session.add(quotation)
        db.session.commit()

        return redirect('/quotations')

    return render_template(
        'quotations/add_quotation.html',
        rfqs=rfqs,
        vendors=vendors
    )


@app.route('/compare_quotations')
def compare_quotations():

    quotation_list = Quotation.query.order_by(
        Quotation.quoted_price.asc()
    ).all()

    return render_template(
        'quotations/compare_quotation.html',
        quotations=quotation_list
    )

# ===================================
# APPROVALS
# ===================================
@app.route('/approvals')
def approvals():
    if 'user_id' not in session:
        return redirect('/login')

    approval_list = Approval.query.all()

    return render_template(
        'approvals/approval_list.html',
        approvals=approval_list
    )


@app.route('/create_approval/<int:quotation_id>')
def create_approval(quotation_id):

    approval = Approval(
        quotation_id=quotation_id,
        status="Approved",
        remarks="Lowest quotation approved"
    )

    db.session.add(approval)
    db.session.commit()

    return redirect('/approvals')

# ===================================
# PURCHASE ORDERS
# ===================================
@app.route('/purchase_orders')
def purchase_orders():

    if 'user_id' not in session:
        return redirect('/login')

    po_list = PurchaseOrder.query.all()

    return render_template(
        'purchase_orders/po_list.html',
        purchase_orders=po_list
    )


@app.route('/generate_po/<int:approval_id>')
def generate_po(approval_id):

    existing_po = PurchaseOrder.query.filter_by(
        approval_id=approval_id
    ).first()

    if existing_po:
        return redirect('/purchase_orders')

    po = PurchaseOrder(
        po_number=f"PO-{approval_id}",
        approval_id=approval_id,
        status="Generated"
    )

    db.session.add(po)
    db.session.commit()

    return redirect('/purchase_orders')

# ===================================
# INVOICES
# ===================================
@app.route('/invoices')
def invoices():

    if 'user_id' not in session:
        return redirect('/login')

    invoice_list = Invoice.query.all()

    return render_template(
        'invoices/invoice_list.html',
        invoices=invoice_list
    )


@app.route('/generate_invoice/<int:po_id>')
def generate_invoice(po_id):

    existing_invoice = Invoice.query.filter_by(
        po_id=po_id
    ).first()

    if existing_invoice:
        return redirect('/invoices')

    invoice = Invoice(
        invoice_number=f"INV-{po_id}",
        po_id=po_id,
        status="Generated"
    )

    db.session.add(invoice)
    db.session.commit()

    return redirect('/invoices')

# ===================================
# EDIT VENDOR
# ===================================
@app.route('/edit_vendor/<int:id>', methods=['GET', 'POST'])
def edit_vendor(id):

    vendor = Vendor.query.get_or_404(id)

    if request.method == 'POST':

        vendor.vendor_name = request.form['vendor_name']
        vendor.email = request.form['email']
        vendor.phone = request.form['phone']
        vendor.category = request.form['category']

        db.session.commit()

        return redirect('/vendors')

    return render_template(
        'vendors/edit_vendor.html',
        vendor=vendor
    )


# ===================================
# DELETE RFQ
# ===================================
@app.route('/delete_rfq/<int:id>')
def delete_rfq(id):

    rfq = RFQ.query.get_or_404(id)

    db.session.delete(rfq)

    db.session.commit()

    return redirect('/rfqs')

# ===================================
# DOWNLOAD INVOICE PDF
# ===================================
@app.route('/download_invoice/<int:invoice_id>')
def download_invoice(invoice_id):

    invoice = Invoice.query.get_or_404(invoice_id)

    buffer = BytesIO()

    pdf = canvas.Canvas(buffer)

    pdf.setTitle(invoice.invoice_number)

    # Safe vendor/rfq lookup
    vendor_name = "N/A"
    rfq_title = "N/A"

    try:
        vendor_name = invoice.purchase_order.approval.quotation.vendor.vendor_name
    except:
        pass

    try:
        rfq_title = invoice.purchase_order.approval.quotation.rfq.title
    except:
        pass

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(200, 800, "VendorBridge ERP")

    pdf.setFont("Helvetica", 14)

    pdf.drawString(
        50,
        740,
        f"Invoice Number: {invoice.invoice_number}"
    )

    pdf.drawString(
        50,
        710,
        f"PO Number: {invoice.purchase_order.po_number}"
    )

    pdf.drawString(
        50,
        680,
        f"Vendor: {vendor_name}"
    )

    pdf.drawString(
        50,
        650,
        f"RFQ: {rfq_title}"
    )

    pdf.drawString(
        50,
        620,
        f"Status: {invoice.status}"
    )

    pdf.drawString(
        50,
        590,
        f"Generated On: {invoice.created_at.strftime('%d-%m-%Y')}"
    )

    pdf.line(50, 560, 550, 560)

    pdf.drawString(
        50,
        530,
        "Thank you for using VendorBridge ERP"
    )

    pdf.save()

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"{invoice.invoice_number}.pdf",
        mimetype='application/pdf'
    )

# ===================================
# DATABASE
# ===================================
with app.app_context():
    db.create_all()

# ===================================
# RUN
# ===================================
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )