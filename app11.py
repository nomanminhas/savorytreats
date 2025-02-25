import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText

# Yahoo SMTP Settings
SMTP_SERVER = "smtp.mail.yahoo.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "noman74ah@yahoo.com"  # Replace with your Yahoo email
EMAIL_PASSWORD = "yyyhekreincqdknv"    # Replace with your generated Yahoo App Password

# Load product data from Excel
@st.cache_data
def load_products():
    df = pd.read_excel("SvaroyTreatPriceList.xlsx")
    return df

products_df = load_products()

# Streamlit UI
st.title("🛒 Shopping Cart System")

# User details
name = st.text_input("Enter your Name")
contact = st.text_input("Enter your Contact Number")

st.header("Select Products")
cart = []

for index, row in products_df.iterrows():
    col1, col2 = st.columns([3, 1])
    with col1:
        quantity = st.number_input(f"{row['Product Name']} - ${row['Unit Price']}", min_value=0, step=1, key=row['Product Name'])
    with col2:
        if quantity > 0:
            cart.append((row['Product Name'], quantity, row['Unit Price'], quantity * row['Unit Price']))

# Display Cart
if cart:
    st.subheader("🛍 Your Shopping Cart")
    cart_df = pd.DataFrame(cart, columns=["Product", "Quantity", "Unit Price", "Total Price"])
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
        except Exception as e:
            st.error(f"❌ Email failed: {e}")

else:
    st.info("🛒 Add items to your cart to proceed.")
