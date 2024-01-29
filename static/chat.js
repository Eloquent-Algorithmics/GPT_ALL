function clearChatHistory() {
    $("#chat-window").empty();
  }
  
  function scrollToBottom() {
    const chatWindow = document.getElementById("chat-window");
    chatWindow.scrollTop = chatWindow.scrollHeight;
  }
  
  $(document).ready(function () {
    $("#chat-form").on("submit", function (event) {
      event.preventDefault();
      const userInput = $("#user-input").val();
      if (userInput.trim() === "") return;
  
      // Display user input in the chat window
      $("#chat-window").append(`<div class="user-message">${userInput}</div>`);
      scrollToBottom(); // Call scrollToBottom() after adding the user message
  
      // Send user input to the server
      $.ajax({
        url: "/process_chat",
        type: "POST",
        data: {
          user_input: userInput,
        },
        success: function (response) {
          // Display AI response in the chat window
          $("#chat-window").append(
            `<div class="ai-message">${response.response}</div>`
          );
          scrollToBottom(); // Call scrollToBottom() after adding the AI message
        },
        error: function (error) {
          console.log(error);
          alert("Error processing chat. Please try again.");
        },
      });
  
      // Clear the input field
      $("#user-input").val("");
    });
  
    $("#clear-chat-btn").on("click", function () {
      clearChatHistory();
    });
  });
  
  $("#chat-form").on("submit", function (event) {
    event.preventDefault();
    var userInput = $("#user-input").val();
    $.post("/send_message", { "user-input": userInput }, function (data) {
      // Append the AI response to the chat window
      $("#chat-window").append(
        '<div class="chat-bubble ai"><p>' + data.ai_response + '</p></div>'
      );
      // Clear the user input field
      $("#user-input").val("");
    });
  });