

### **Step-by-Step Deployment Guide for AWS EC2**



### **Step 1: Launch an EC2 Instance**
1. **Log in to AWS EC2 Console**:
   Go to [AWS EC2 Console](https://console.aws.amazon.com/ec2/).

2. **Launch a New Instance**:
   - Select **Amazon Linux 2 AMI** (or another Linux distribution).
   - Choose **t2.micro** or another instance type.
   - Configure instance details as per your need.
   - In the **Security Group** settings:
     - Add a rule to allow **SSH (port 22)**.
     - Add a rule for **HTTP (port 80)** if you want to expose it to the web.
     - Add a rule for **Custom TCP (port 8000)** to run Django locally (for testing).

3. **Connect to Your EC2 Instance**:
   Once the instance is running, connect using SSH. If you're using a `.pem` key file:
   ```bash
   ssh -i <your-key.pem> ec2-user@<your-ec2-public-ip>
   ```

---

### **Step 2: Update the EC2 Instance**
1. Once connected to your EC2 instance, update the system:
   ```bash
   sudo yum update -y
   ```

---

### **Step 3: Install Required Software**
1. **Install Python 3 and PIP**:
   ```bash
   sudo yum install python3 -y
   sudo yum install python3-pip -y
   ```

2. **Install Git** (to clone the repository):
   ```bash
   sudo yum install git -y
   ```

3. **Install PostgreSQL** (only if your Django project uses PostgreSQL, otherwise skip this):
   ```bash
   sudo yum install postgresql postgresql-server postgresql-devel -y
   ```

---

### **Step 4: Set Up a Virtual Environment**
1. **Install `virtualenv`**:
   ```bash
   sudo pip3 install virtualenv
   ```

2. **Create a New Directory for the Project**:
   ```bash
   mkdir cryptocurrency-price-prediction
   cd cryptocurrency-price-prediction
   ```

3. **Create a Virtual Environment**:
   ```bash
   python3 -m venv venv
   ```

4. **Activate the Virtual Environment**:
   ```bash
   source venv/bin/activate
   ```

   After activating the environment, your prompt will change to indicate you're in the virtual environment.

---

### **Step 5: Clone the Repository**
1. **Clone Your GitHub Repository**:
   ```bash
   git clone https://github.com/Hugs-4-Bugs/Cryptocurrency-Price-prediction-using-ML.git
   cd Cryptocurrency-Price-prediction-using-ML
   ```

---

### **Step 6: Install Required Python Libraries**
1. **Install Dependencies from `requirements.txt`**:
   If the `requirements.txt` is available in your project, you can install all required libraries:
   ```bash
   pip install -r requirements.txt
   ```

   If `requirements.txt` is missing, install the libraries manually:
   ```bash
   pip install pandas numpy scikit-learn matplotlib tensorflow keras django
   ```

---

### **Step 7: Configure Database (Optional, If Using PostgreSQL)**

If your Django project uses PostgreSQL as a database, follow these steps:

1. **Start PostgreSQL**:
   ```bash
   sudo service postgresql start
   ```

2. **Create a New PostgreSQL Database and User**:
   ```bash
   sudo -u postgres psql
   CREATE DATABASE mydb;
   CREATE USER myuser WITH PASSWORD 'mypassword';
   ALTER ROLE myuser SET client_encoding TO 'utf8';
   ALTER ROLE myuser SET default_transaction_isolation TO 'read committed';
   ALTER ROLE myuser SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;
   \q
   ```

3. **Configure Django to Use PostgreSQL**:
   Update the `DATABASES` setting in `settings.py` to match the PostgreSQL credentials.

---

### **Step 8: Apply Migrations**
1. **Run Migrations**:
   This step sets up the database schema for your Django project.
   ```bash
   python3 manage.py migrate
   ```

---

### **Step 9: Create a Superuser**
1. **Create Django Superuser**:
   This allows you to log into Django's admin panel.
   ```bash
   python3 manage.py createsuperuser
   ```

   Follow the prompts to create the superuser (username, email, password).

---

### **Step 10: Run the Django Development Server**
1. **Start the Django Server** (for testing purposes):
   ```bash
   python3 manage.py runserver 0.0.0.0:8000
   ```

   You can now access your application at `http://<your-ec2-public-ip>:8000`.

---

### **Step 11: Set Up Production Environment (Optional)**

For a production environment, you should run **Gunicorn** with **Nginx** as a reverse proxy:

1. **Install Gunicorn**:
   ```bash
   pip install gunicorn
   ```

2. **Run Gunicorn**:
   ```bash
   gunicorn --workers 3 --bind 0.0.0.0:8000 cryptocurrency_price_prediction.wsgi:application
   ```

3. **Install Nginx**:
   ```bash
   sudo yum install nginx -y
   ```

4. **Configure Nginx** to Proxy Requests to Gunicorn:
   Create a new Nginx configuration file:
   ```bash
   sudo vi /etc/nginx/conf.d/cryptocurrency_price_prediction.conf
   ```

   Add the following configuration:

   ```nginx
   server {
       listen 80;
       server_name <your-ec2-public-ip>;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

5. **Start Nginx**:
   ```bash
   sudo service nginx start
   ```

   **Optional**: Set Nginx to start on boot:
   ```bash
   sudo systemctl enable nginx
   ```

---

### **Step 12: Set Up SSL for HTTPS (Optional)**
To secure your site with HTTPS, use **Let's Encrypt** and **Certbot** to install SSL certificates:

1. **Install Certbot**:
   ```bash
   sudo yum install certbot
   ```

2. **Get SSL Certificates**:
   ```bash
   sudo certbot --nginx
   ```

   Follow the prompts to obtain and configure the SSL certificates.

---

### **Step 13: Stop the Development Server (Optional)**
If you were running the Django development server (with `python manage.py runserver`), you can stop it by pressing `Ctrl+C` in the terminal.

In production, you should use Gunicorn or another production-grade WSGI server.

---

### **Step 14: Access Your Django Admin Panel**
Once the server is running, access your admin panel by navigating to:

```
http://<your-ec2-public-ip>/admin
```

Log in using the superuser credentials you created earlier.

---

### **Step 15: (Optional) Set Up a Firewall (Security Groups)**
Ensure your EC2 instance's **Security Groups** allow the necessary traffic:
- **Port 22 (SSH)**: For SSH access.
- **Port 80 (HTTP)**: For serving the web application.
- **Port 443 (HTTPS)**: For secure connections (if you set up SSL).
- **Port 8000**: For Django development server access (if necessary).

