function predict() {
    const word = document.getElementById('inputWord').value;
    console.log('Word to predict:', word);  // Debug: print the word to predict
    fetch('http://localhost:5000/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ word }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Server response:', data);  // Debug: print the server response
        if (data.error) {
            alert(data.error);
        } else {
            const predictedWord = data.predicted_word;
            console.log('Predicted word:', predictedWord);  // Debug: print the predicted word
            document.getElementById('inputTextArea').value = 'Predicted word: ' + predictedWord;
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

window.onload = function() {
    document.getElementById("predictButton").addEventListener("click", predict);
};