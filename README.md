# PresencePulse : Face Recognition Based Automated Attendance System


![Alt Text](https://github.com/suyash-rgb/PresencePulse/blob/7546e56fd96b26c27631b5953fbf2097e517c7eb/Images/photo_2024-12-11_11-28-26.jpg)

# Project Description

**PresencePulse** is an innovative face recognition-based automated attendance system designed to streamline the process of attendance tracking in educational institutions and workplaces. Using cutting-edge face recognition technology, PresencePulse aims to enhance accuracy and efficiency in recording attendance.

Structure of the PresencePulse GUI Application: <br> <br>

![Alt Text](https://github.com/suyash-rgb/PresencePulse/blob/1a44656d96c2c7ef4534544058aa45887c14b9c1/Images/PresencePulse%20GUI%20Structure%20and%20Workflow.png)



# Setup Instructions

## Setting Up OAuth Client ID in Google Cloud Console

1. **Go to Google Cloud Console**: Visit the [Google Cloud Console](https://console.cloud.google.com/) and log in with your Google account.

2. **Create or Select a Project**: On the project selector page, select an existing project or create a new one.

3. **Enable APIs & Services**: In the left sidebar, click on "APIs & Services" and then select "Library".

4. **Enable Google Sheets API**: Search for "Google Sheets API" and enable it.

5. **Create Credentials**: Go to "Credentials" and click on "Create Credentials".

6. **Select OAuth Client ID**: Choose "OAuth client ID" from the options.

7. **Configure Consent Screen**: If prompted, configure the consent screen by providing the necessary information like product name, support email, etc.

8. **Create Client ID**: Choose "Web application" as the application type. Add your ngrok domain to the "Authorized redirect URIs" and "Authorized JavaScript origins". Click "Create" to generate the OAuth client ID. Note down the client ID and client secret.

## Using ngrok to Claim a Static Domain

1. **Sign Up for ngrok**: If you don't have an ngrok account, sign up for one on the [ngrok website](https://ngrok.com/).

2. **Log In to ngrok**: Log in to your ngrok account.

3. **Navigate to Domains**: Go to "Cloud Edge" and select "Domains".

4. **Claim Your Static Domain**: Follow the prompts to claim your unique, static domain.

5. **Use Your Static Domain**: Start ngrok with your static domain using the command: <br>
    ngrok http --domain=[your-static-domain] 80 


# Understanding ngrok and ngrok Tunnels

## What is ngrok?
ngrok is a powerful tool that allows you to create secure tunnels to your local server, making it accessible from the internet. It is particularly useful for testing webhooks, APIs, and local development projects without needing to deploy them to a remote server.

## What is an ngrok Tunnel?
An ngrok tunnel is a secure, encrypted connection created by ngrok that allows external access to a locally hosted server. When you run ngrok, it assigns a public URL to your local server, enabling anyone with the URL to access your local application. This is extremely useful for:

- **Development and Testing**: Quickly sharing your local development environment with collaborators or clients.
- **API Integration**: Testing webhooks and API integrations that require public URL callbacks.
- **IoT and Device Management**: Connecting IoT devices running in external networks.


# Contributing

If you'd like to contribute to this repository, please follow these guidelines:

1. **Fork the repository.**
2. **Create a new branch** (e.g., `git checkout -b feature/your-feature`).
3. **Commit your changes** (e.g., `git commit -m 'Add your feature'`).
4. **Push to the branch** (e.g., `git push origin feature/your-feature`).
5. **Open a Pull Request.**

# Contact

If you have any questions, feel free to reach out:

- **Email**: suyashbaoney58@gmail.com
- **LinkedIn**: [your-linkedin-profile](www.linkedin.com/in/suyash-baoney-bb38b3290)
