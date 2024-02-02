$(document).ready(function () {
  function clearChatHistory() {
      $("#chat-window").empty();
  }

  function scrollToBottom() {
      const chatWindow = $("#chat-window")[0];
      chatWindow.scrollTop = chatWindow.scrollHeight;
  }

  let memory = [];

  function showTypingAnimation() {
      const typingDots = '<span>.</span><span>.</span><span>.</span>';
      $("#chat-window").append(`<div class="message-wrapper ai" id="typing-animation"><img class="aiavatar" src="${aiAvatarUrl}" /><div class="ai-message">${typingDots}</div></div>`);
      scrollToBottom();
  }

  function removeTypingAnimation() {
      $("#typing-animation").remove();
  }

  // Preload images
  function preloadImages() {
      const imagesToPreload = ["/static/U1.webp", "/static/J5.webp"];
      imagesToPreload.forEach(imageSrc => {
          const img = new Image();
          img.src = imageSrc;
      });
  }

  preloadImages();

  $("#input-form").submit(async function (event) {
      event.preventDefault();
      const userText = $("#user-input").val().trim();
      if (!userText) return;

      $("#chat-window").append(`<div class="message-wrapper user"><div class="user-message">${userText}</div><img class="useravatar" src="${userAvatarUrl}" /></div>`);
      $("#user-input").val("");

      showTypingAnimation();

      try {
          const response = await $.ajax({
              url: "/chat", // Make sure this endpoint is correct
              type: "POST",
              contentType: "application/json",
              data: JSON.stringify({ user_input: userText, memory }),
          });

          removeTypingAnimation();
          $("#chat-window").append(`<div class="message-wrapper ai"><img class="aiavatar" src="${aiAvatarUrl}" /><div class="ai-message">${response.response}</div></div>`);
          memory = response.memory;
          scrollToBottom();
      } catch (error) {
          console.error("Error: Unable to get a response from the assistant.", error);
          $("#chat-window").append(`<div class="message-wrapper ai"><div class="ai-message">Error: Unable to get a response from the assistant.</div></div>`);
      }
  });

  $("#clear-chat-btn").click(function () {
      clearChatHistory();
  });
});