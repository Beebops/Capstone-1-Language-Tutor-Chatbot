$('#submit-button').click(function () {
  const question = $('#user-input').val()

  let htmlData = ''

  htmlData += `
  <div
        class="bg-secondary list-group-item list-group-item-action d-flex gap-3 py-3"
      >
        <p class="fs-1">&#128512;</p>
        <p id="user-text" class="mb-0 opacity-75">
          ${question}
        </p>
      </div>
`
  $('#user-input').val('')

  $('#list-group').append(htmlData)
})
