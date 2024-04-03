<h1>Smart Doorbell Project</h1>

<h2>Features</h2>
<ul>
 <li>Encryption for images: Ensures that captured images are stored securely.</li>
 <li>Facial Recognition using OpenCV Pretrained Classifier: Allows the system to recognize faces efficiently.</li>
 <li>Encrypted images are pushed to Firebase Storage Cloud</li>
 <li>Authentication using email and password</li>
 <li>A cross-platform mobile app that includes:
   <ul>
     <li>Implement remote notification using cloud services for real-time alerts.(Android Only)</li>
     <li>Display of historical data, such as unrecognized faces.</li>
   </ul>
 </li>
</ul>

<h2>Todo</h2>
<ul>
 <li>Add motion sensor to only start facial recognition when motion is detected. This helps in saving resources.</li>
 <li>Implement a system to "ring" the doorbell when certain conditions are met (e.g., an unrecognized face is detected).</li>
 <li>Conduct thorough testing under different conditions, such as varying lighting conditions and different faces, to ensure reliability and robustness.</li>
</ul>

<h2>Installation on Pi400</h2>
<p>Activate python environment</p>
<pre><code>source <yourenvname>/bin/activate</code></pre>

<p>Activate python environment (Use this if you follow Lab 1 environment creation)</p>
<pre><code>source myenv/bin/activate</code></pre>

<p>Run the following commands to install the required packages:</p>
<pre><code>sudo apt-get update
pip install --upgrade pip
pip install numpy Pillow opencv-python-headless cryptography opencv-contrib-python pyrebase4 torch torchvision torchaudio
</code></pre>

<p>Before running, please ask for <code>service account json</code>,<code>server.txt</code> and <code>data.txt</code> as i am unable to upload to GitHub. Put in project root folder.</p>

<h2>Running</h2>
<ol>
<li>Registering face</li>
<pre><code>python register.py</code></pre>

<li>Training Model (need to do after every new face)</li>
<pre><code>python train.py</code></pre>

<li>Recognising</li>
<pre><code>python recognise.py</code></pre>
</ol>
