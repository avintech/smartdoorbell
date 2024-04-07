<h1>Smart Doorbell Project</h1>

<h2>Features</h2>
<ul>
 <li>Encryption for images: Ensures that captured images are stored securely.</li>
 <li>Facial Recognition using OpenCV Pretrained Classifier: Allows the system to recognize faces efficiently.</li>
 <li>Object Detection using Yolo5</li>
 <li>Obstruction Detection</li>
 <li>Encrypted images are pushed to Firebase Storage Cloud</li>
 <li>Authentication using email and password</li>
 <li>A cross-platform mobile app that includes:
   <ul>
     <li>Implement remote notification using cloud services for real-time alerts.(Android Only)</li>
     <li>Display of historical data, such as unrecognized faces.</li>
   </ul>
 </li>
</ul>

<h2>Installation on Pi400</h2>
<p>This project was tested on Python 3.9.19, you can follow these instructions to install.</p>
<ol>
  <li>Run in Terminal</li>
  <pre><code>curl https://pyenv.run | bash
  pyenv install -v 3.9.19</code></pre>
  <li>Tea</li>
  <li>Milk</li>
</ol>

<p>Activate python environment</p>
<pre><code>source <yourenvname>/bin/activate</code></pre>

<p>Activate python environment (Use this if you follow Lab 1 environment creation)</p>
<pre><code>source myenv/bin/activate</code></pre>

<p>Run the following commands to install the required packages:</p>
<pre><code>sudo apt-get update
pip install --upgrade pip
pip install numpy Pillow cryptography opencv-contrib-python pyrebase4 torch torchvision torchaudio pandas
</code></pre>

<p>Before running, please ask for Google Credentials as i am unable to upload to GitHub for security reasons. Put in respective folders in the directory.</p>

<h2>Running</h2>
<ol>
<li>Registering face</li>
<pre><code>python register.py</code></pre>

<li>Recognising</li>
<pre><code>python recognise.py</code></pre>
</ol>
