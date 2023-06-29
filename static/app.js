const chatId = $('#message-group').data('chatId')

$('#submit-button').click(async function () {
  const message = $('#user-input').val()

  let htmlData = `
    <li class="list-group-item my-1">
      <div class="row align-items-center">
        <div class="col-auto">
          <span class="fs-3">&#128512;</span>
        </div>
        <div class="col">
          <span id="user-text" class="opacity-75">${message}</span>
        </div>
      </div>
    </li>
  `

  $('#user-input').val('')
  $('#message-group').append(htmlData)

  try {
    const response = await axios.post(`/chat/${chatId}`, { prompt: message })

    let apiData = `
      <li class="list-group-item my-1">
        <div class="row align-items-center">
          <div class="col-auto">
            <span class="fs-3">&#127891;</span>
          </div>
          <div class="col">
            <span id="user-text" class="opacity-75">${response.data.assistant_message}</span>
          </div>
        </div>
      </li>
    `

    $('#message-group').append(apiData)
    console.log(message)
  } catch (error) {
    // Handle error
    alert('Uh oh! We are experiencing technical difficulties. Try again later')
    console.error(error)
  }
})
