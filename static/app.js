// need to figure out how to get the logged in user's id programmatically
const userId = '1'

$('#submit-button').click(function () {
  const message = $('#user-input').val()

  let htmlData = ''

  htmlData += `
  <div
        class="bg-secondary list-group-item list-group-item-action d-flex gap-3 py-3"
      >
        <p class="fs-1">&#128512;</p>
        <p id="user-text" class="mb-0 opacity-75">
          ${message}
        </p>
      </div>
`
  $('#user-input').val('')

  $('#list-group').append(htmlData)

  // call the server to get tutor message
  $.ajax({
    type: 'POST',
    url: `/chat/${userId}`,
    data: { prompt: message },
    success: function (data) {
      let apiData = ''
      apiData += `
      <div
        class="bg-secondary list-group-item list-group-item-action d-flex gap-3 py-3"
      >
        <p class="fs-1">&#127891;</p>
        <p id="user-text" class="mb-0 opacity-75">
          ${data.message}
        </p>
      </div>
      `
      $('#list-group').append(apiData)
    },
  })
})
