<h1>Smart Doorbell Project</h1>

<h2>Features</h2>
<ul>
 <li>AES Encryption for images: Ensures that captured images are stored securely.</li>
 <li>Facial Recognition using OpenCV Pretrained Classifier: Allows the system to recognize faces efficiently.</li>
</ul>

<h2>Todo</h2>
<ul>
 <li>Add motion sensor to only start facial recognition when motion is detected. This helps in saving resources.</li>
 <li>Implement remote notification using cloud services (e.g., Firebase Cloud Messaging) for real-time alerts.</li>
 <li>Develop a dashboard for data representation, which might include:
   <ul>
     <li>Live footage display.</li>
     <li>Recognition status indication.</li>
     <li>Display of historical data, such as unrecognized faces.</li>
   </ul>
 </li>
 <li>Develop a mobile app, which might include:
   <ul>
     <li>Push notifications</li>
     <li>Display of historical data, such as unrecognized faces.</li>
   </ul>
 </li>
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
pip install numpy Pillow opencv-python-headless pycryptodome opencv-contrib-python pyrebase
</code></pre>

<h2>Running</h2>
<ol>
<li>Registering face</li>
<pre><code>python register.py</code></pre>

<li>Training Model (need to do after every new face)</li>
<pre><code>python train.py</code></pre>

<li>Recognising</li>
<pre><code>python recognise.py</code></pre>
</ol>
