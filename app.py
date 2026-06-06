from flask import Flask, render_template, request, redirect
from models import db, Vendor, RFQ

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

    return render_template(
        'dashboard.html',
        total_vendors=total_vendors,
        total_rfqs=total_rfqs
    )


# ===================================
# VENDOR LIST
# ===================================
@app.route('/vendors')
def vendors():

    vendor_list = Vendor.query.all()

    return render_template(
        'vendors/vendor_list.html',
        vendors=vendor_list
    )


# ===================================
# ADD VENDOR
# ===================================
@app.route('/add_vendor', methods=['GET', 'POST'])
def add_vendor():

    if request.method == 'POST':

        new_vendor = Vendor(
            vendor_name=request.form['vendor_name'],
            email=request.form['email'],
            phone=request.form['phone'],
            gst_number=request.form['gst_number'],
            category=request.form['category']
        )

        db.session.add(new_vendor)
        db.session.commit()

        return redirect('/vendors')

    return render_template(
        'vendors/add_vendor.html'
    )


# ===================================
# DELETE VENDOR
# ===================================
@app.route('/delete_vendor/<int:id>')
def delete_vendor(id):

    vendor = Vendor.query.get_or_404(id)

    db.session.delete(vendor)

    db.session.commit()

    return redirect('/vendors')


# ===================================
# RFQ LIST
# ===================================
@app.route('/rfqs')
def rfqs():

    rfq_list = RFQ.query.all()

    return render_template(
        'rfq/rfq_list.html',
        rfqs=rfq_list
    )


# ===================================
# CREATE RFQ
# ===================================
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
# DATABASE
# ===================================
with app.app_context():
    db.create_all()


# ===================================
# RUN
# ===================================
if __name__ == "__main__":

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )