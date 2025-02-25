import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText

# Yahoo SMTP Settings
SMTP_SERVER = "smtp.mail.yahoo.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "noman74ah@yahoo.com"  # Replace with your Yahoo email
EMAIL_PASSWORD = "yyyhekreincqdknv"    # Replace with your Yahoo App Password

# Load product data from Excel
@st.cache_data
def load_products():
    df = pd.read_excel("SvaroyTreatPriceList.xlsx")
    return df

products_df = load_products()

# Initialize session state for cart
if "cart" not in st.session_state:
    st.session_state.cart = []

# Streamlit UI
st.title("🛒 Shopping Cart System")

# User details
name = st.text_input("Enter your Name")
contact = st.text_input("Enter your Contact Number")

st.header("Select Products")

# Dropdown for product selection
selected_product = st.selectbox("Choose a product to add", ["Select a product"] + list(products_df["Product Name"].unique()))

if selected_product != "Select a product":
    quantity = st.number_input(f"Enter quantity for {selected_product}", min_value=1, step=1, key=selected_product)
    if st.button("➕ Add to Cart"):
        price = products_df.loc[products_df["Product Name"] == selected_product, "Unit Price"].values[0]
        total_price = quantity * price

        # Add product to cart in session state
        st.session_state.cart.append((selected_product, quantity, price, total_price))
        st.success(f"✅ {selected_product} added to cart!")

# Display Cart
if st.session_state.cart:
    st.subheader("🛍 Your Shopping Cart")
    cart_df = pd.DataFrame(st.session_state.cart, columns=["Product", "Quantity", "Unit Price", "Total Price"])
    st.table(cart_df)

    grand_total = cart_df["Total Price"].sum()
    st.write(f"### 💰 Grand Total: ${grand_total:.2f}")

    # Send Order via Email
    if st.button("📩 Place Order & Email Cart"):
        cart_details = cart_df.to_string(index=False)
        email_body = f"Name: {name}\nContact: {contact}\n\nCart Details:\n{cart_details}\n\nTotal: ${grand_total:.2f}"

        msg = MIMEText(email_body)
        msg["Subject"] = "New Order Received"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS  # Send to yourself

        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg.as_string())
            st.success("✅ Order placed successfully! Check your email.")
            st.session_state.cart = []  # Clear cart after order is placed
        except Exception as e:
            st.error(f"❌ Email failed: {e}")

else:
    st.info("🛒 Add items to your cart to proceed.")
