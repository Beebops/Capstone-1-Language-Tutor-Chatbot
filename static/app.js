// need to figure out how to get the logged in user's id programmatically

const chatId = $('#message-group').data('chatId')

$('#submit-button').click(async function () {
  const message = $('#user-input').val()

  let htmlData = `
    <div class="bg-secondary list-group-item list-group-item-action d-flex gap-3 py-3 border border-light border-1">
      <p class="fs-1">&#128512;</p>
      <p id="user-text" class="mb-0 opacity-75">
        ${message}
      </p>
    </div>
  `
  $('#user-input').val('')
  $('#message-group').append(htmlData)

  try {
    const response = await axios.post(`/chat/${chatId}`, { prompt: message })
    let apiData = `
      <div class="bg-secondary list-group-item list-group-item-action d-flex gap-3 py-3 border border-light border-1">
        <p class="fs-1">&#127891;</p>
        <p id="user-text" class="mb-0 opacity-75">
          ${response.data.assistant_message}
        </p>
      </div>
    `
    $('#message-group').append(apiData)
    console.log(message)
  } catch (error) {
    // Handle error
    alert('Oh uh! We are experiencing technical difficulties. Try again later')
    console.error(error)
  }
})
