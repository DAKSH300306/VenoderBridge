from flask import Flask, render_template, request, redirect
from models import db, Vendor, RFQ, Quotation, Approval, PurchaseOrder, Invoice

app = Flask(__name__)

# ===================================
# CONFIG
# ===================================
app.config['SECRET_KEY'] = 'vendorbridge_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vendorbridge.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# ===================================
# DASHBOARD
# ===================================
@app.route('/')
def dashboard():

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

    po_list = PurchaseOrder.query.all()

    return render_template(
        'purchase_orders/po_list.html',
        purchase_orders=po_list
    )


@app.route('/generate_po/<int:approval_id>')
def generate_po(approval_id):

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

    invoice_list = Invoice.query.all()

    return render_template(
        'invoices/invoice_list.html',
        invoices=invoice_list
    )


@app.route('/generate_invoice/<int:po_id>')
def generate_invoice(po_id):

    invoice = Invoice(
        invoice_number=f"INV-{po_id}",
        po_id=po_id,
        status="Generated"
    )

    db.session.add(invoice)
    db.session.commit()

    return redirect('/invoices')

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