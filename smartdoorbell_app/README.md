<body>

<h1>Project README</h1>

<h2>Introduction</h2>

<p>This project README provides essential information regarding the setup of Google Services JSON files required for both iOS and Android platforms.</p>

<h3>Required Google Services JSON Files</h3>

<p>To properly integrate Google services into your application, ensure that you have the following JSON files included in your project directory:</p>

<ol>
<li>
    <strong>iOS Notification Setup</strong>
    <ul>
    <li>iOS Notification does not work due to the absence of an Apple Developer Account.</li>
    <li>Place the following files under the specified directories:</li>
    <ul>
        <li><code>ios/firebase_app_id_file.json</code></li>
        <li><code>ios/Runner/GoogleService-Info.plist</code></li>
    </ul>
    </ul>
</li>
<li>
    <strong>Android Google Services JSON</strong>
    <ul>
    <li>Place the following file under the specified directory:</li>
    <ul>
        <li><code>android/app/google-services.json</code></li>
    </ul>
    </ul>
</li>
</ol>

<p><strong>Note:</strong> Please note that iOS notification services require an Apple Developer Account for proper functionality. Without it, notifications may not work as expected on iOS devices.</p>

<h2>Instructions</h2>

<p>To set up the project correctly, follow these steps:</p>

<ol>
<li>
    <strong>iOS Setup:</strong>
    <ul>
    <li>Place the <code>firebase_app_id_file.json</code> and <code>GoogleService-Info.plist</code> files in the respective directories as mentioned above under the <code>ios</code> directory.</li>
    </ul>
</li>
<li>
    <strong>Android Setup:</strong>
    <ul>
    <li>Place the <code>google-services.json</code> file under the <code>android/app</code> directory.</li>
    </ul>
</li>
<li>
    <strong>Additional Steps:</strong>
    <ul>
    <li>Ensure that all necessary configurations for Firebase and Google services are properly set up in your project.</li>
    </ul>
</li>
</ol>

<h2>Troubleshooting</h2>

<p>If you encounter any issues with notifications on iOS or integration with Firebase and Google services on either platform, double-check that the JSON files are correctly placed in the designated directories and that your Firebase and Apple Developer Account configurations are correct.</p>

<p>For further assistance, refer to the official documentation of Firebase and Google services or consult relevant forums and communities.</p>

</body>
</html>
