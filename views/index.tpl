<!DOCTYPE html>
<html>
<head>
<title>Test</title>
<script src="//ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js">
  </script>
  <script type="text/javascript">
    (function () {
      var po = document.createElement('script');
      po.type = 'text/javascript';
      po.async = true;
      po.src = 'https://plus.google.com/js/client:plusone.js?onload=start';
      var s = document.getElementsByTagName('script')[0];
      s.parentNode.insertBefore(po, s);
    })();
  </script>
</head>
<body>
<div id="signinButton">
<span class="g-signin" style="display: none"
    data-scope="https://www.googleapis.com/auth/plus.login"
    data-clientid="{{client_id}}"
    data-redirecturi="postmessage"
    data-accesstype="offline"
    data-cookiepolicy="single_host_origin"
    data-callback="signInCallback">
  </span>
</div>
<div id="results"></div>
<a href="javascript:void(0)" id="revokeButton" style="display: none">Logout</a>

<script type="text/javascript">
function signInCallback(authResult) {
  if (authResult['code']) {
    // Hide the sign-in button, and show the logout button 
    $('#signinButton').attr('style', 'display: none');
    $('#revokeButton').attr('style', 'display: inline');
    $('#revokeButton').click(function () {
      disconnectUser(authResult['access_token']);
    });

    // Send the code to the server
    $.ajax({
      type: 'POST',
      url: '/connect?state={{state}}',
      contentType: 'application/octet-stream; charset=utf-8',
      success: function(result) {
        // Render the information returned by the server in the info div.
        console.log(result);
        if (result['info'] ){
          $('#results').html(result['info']);
        } else {
          $('#results').html('Failed to make a server-side call. Check your configuration and console.');
        }
      },
      processData: false,
      data: authResult['code']
    }); 
  } else if (authResult['error']) {
    // There was an error.
    // Possible error codes:
    //   "access_denied" - User denied access to your app
    //   "immediate_failed" - Could not automatially log in the user
    console.log('There was an error: ' + authResult['error']);
    console.log('An immediate_failed error is expected when a new user loads the page.');
    $('#signinButton').attr('style','display: inline');
    $('#revokeButton').attr('style','display: none');
  }
}

function disconnectUser(access_token) {
  var revokeUrl = 'https://accounts.google.com/o/oauth2/revoke?token=' +
      access_token;

  // Perform an asynchronous GET request.
  $.ajax({
    type: 'GET',
    url: revokeUrl,
    async: false,
    contentType: "application/json",
    dataType: 'jsonp',
    success: function(nullResponse) {
      // Hide the logout button, show the sign-in button, and get rid of the user info
      // when successfully logged out.
      $('#revokeButton').attr('style','display: none');
      $('#signinButton').attr('style','display: inline');
      $('#results').html('');
    },
    error: function(e) {
      // Handle the error, I imagine a network connection error would get you to this point.
      console.log(e);
    }
  });
}
</script>

</body>
</html>
