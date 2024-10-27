# Remote Python Script Executor

This project consists of two scripts that work together to securely fetch and execute a remote Python script. It's useful for scenarios where you need to execute code hosted remotely.

## Table of Contents

- [Overview](#overview)
- [Files](#files)
  - [url_execution.py](#url_executionpy)
  - [worker.js](#workerjs)
- [Setup and Usage](#setup-and-usage)
  - [Setting Up the Worker Script](#setting-up-the-worker-script)
  - [Running the Python Script](#running-the-python-script)
- [Security Considerations](#security-considerations)
- [Use Cases](#use-cases)
- [License](#license)

## Overview

The solution allows you to host a Python script on a server (using `worker.js`) and fetch it securely from a client script (`url_execution.py`). The client script downloads the remote script, normalizes its indentation, and executes it locally.

## Files

### url_execution.py

This Python script performs the following actions:

1. **Fetches a Remote Script**: Uses `urllib.request` to make an HTTP request to a specified URL.
2. **Normalizes Indentation**: Adjusts the indentation of the downloaded script to ensure it executes correctly.
3. **Executes the Script**: Uses `exec()` to run the downloaded script in the global namespace.

#### Key Functions:

- `i_wasnt(url)`: Fetches content from the provided URL with custom headers and SSL context to handle certificates.
- `normalize_indentation(content)`: Removes leading spaces to normalize the indentation of the script.
- `even_there()`: Main function that fetches, cleans, and executes the remote script.

### worker.js

This JavaScript script is designed to be deployed on a server (e.g., using serverless functions or a Node.js server). It serves the Base64-encoded Python script when requested.

#### How It Works:

- **Event Listener**: Listens for `fetch` events and responds with the `handleRequest` function.
- **Base64-Encoded Script**: Contains a Base64-encoded version of the Python script you want to serve.
- **Response**: Decodes the script and sends it as a downloadable file with appropriate headers.

## Setup and Usage

### Setting Up the Worker Script

1. **Encode Your Python Script**:

   - Encode the Python script you wish to serve in Base64:

     ```bash
     base64 your_script.py > encoded_script.txt
     ```

   - On Windows, you can use PowerShell:

     ```powershell
     [Convert]::ToBase64String([IO.File]::ReadAllBytes("your_script.py")) > encoded_script.txt
     ```

2. **Update `worker.js`**:

   - Replace the placeholder in `pythonScriptBase64` with the contents of `encoded_script.txt`:

     ```javascript
     const pythonScriptBase64 = `
     <your Base64-encoded script here>
     `;
     ```

3. **Deploy the Worker Script**:

   - Deploy `worker.js` to your server or serverless platform (e.g., Cloudflare Workers).

     - **Cloudflare Workers**:

       - Log in to your Cloudflare account.
       - Navigate to the **Workers** section.
       - Create a new worker and paste the contents of your updated `worker.js`.
       - Save and deploy the worker.

     - **AWS Lambda** (with API Gateway):

       - Create a new Lambda function using Node.js.
       - Paste the contents of `worker.js` into the function code.
       - Set up an API Gateway to trigger the Lambda function.

     - **Node.js Server**:

       - Set up an Express.js application.
       - Include the logic from `worker.js` in a route handler.

4. **Test the Endpoint**:

   - Access the URL where the worker script is deployed to ensure it serves the Python script correctly.

### Running the Python Script

1. **Update `url_execution.py`**:

   - Replace `"your url here"` with the URL where your worker script is accessible:

     ```python
     url = "https://your-worker-url.example.com"
     ```

2. **Run `url_execution.py`**:

   ```bash
   python url_execution.py
   ```
The script will fetch the remote Python code, normalize its indentation, and execute it.
Security Considerations
### Execution Risks: 
Using exec() to run remote code is inherently risky. Ensure that the remote script is from a trusted source.

### SSL Verification: 
The script uses an unverified SSL context (ssl._create_unverified_context()). For better security, modify the script to verify SSL certificates:

```python
context = ssl.create_default_context()
```
###Content Sanitization: 
The script normalizes indentation but does not sanitize the content. Be cautious about code injection.

### HTTPS Connection: 
Ensure the URL uses HTTPS to prevent man-in-the-middle attacks.

## Use Cases
### Dynamic Code Updates: 
Fetch updated code without redistributing the client script.
### Centralized Control: 
Centralize control over scripts executed by multiple clients.
### Educational Purposes: 
Demonstrate remote code execution and handling in Python.

## License
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

### Disclaimer: The software is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringement. In no event shall the authors or copyright holders be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the software or the use or other dealings in the software.

### Additional Information

- **worker.js Deployment**:

  Since `worker.js` is the code running on the URL hosting the remote code, it's essential to deploy it properly:

  - **Cloudflare Workers**:

    - Ideal for this use case due to their simplicity and ease of deployment.
    - Offers free tiers for personal projects.

  - **Serverless Platforms**:

    - Platforms like AWS Lambda, Azure Functions, or Google Cloud Functions can host `worker.js`.

  - **Traditional Server**:

    - If you have a Node.js server, you can integrate `worker.js` logic into your application.

- **Testing the Setup**:

  After deploying `worker.js`, you can test it by visiting the URL in a browser. It should prompt you to download the Python script (named `file-name.py` as specified in the headers).

- **Customizing the Python Script**:

  - Ensure that the Python script you encode does not contain any sensitive information.
  - Update the filename in the `Content-Disposition` header if needed:

    ```javascript
    'Content-Disposition': 'attachment; filename="your_script_name.py"',
    ```

### Security Best Practices

- **Validate SSL Certificates**:

  In `url_execution.py`, use a verified SSL context:

  ```python
  context = ssl.create_default_context()
  ```
## Handle Exceptions:

Wrap your code in try-except blocks to handle potential exceptions during network requests or execution.

```python
try:
    content = i_wasnt(url)
    # Rest of your code...
except Exception as e:
    print(f"An error occurred: {e}")
```
## Limit Execution Scope:

### Use a restricted dictionary for exec() to limit the scope:

```python
exec(cleaned_content, {'__builtins__': None}, {})
```
Note that you may need to allow certain built-in functions depending on your script's needs.

## Disclaimer
### Security Risks:

Executing code fetched over the network can be dangerous. Only use this setup with code from trusted sources.

## SSL Context:

The provided url_execution.py script disables SSL verification. Modify it to enable SSL verification in production environments.
