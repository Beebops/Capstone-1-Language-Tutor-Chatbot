$(document).ready(function () {
  // Handle language selection change
  $('#language-select').on('change', function () {
    var selectedLanguage = $(this).val()
    filterChatsByLanguage(selectedLanguage)
  })

  function filterChatsByLanguage(language) {
    $('#chat-list li').each(function () {
      var chatLanguage = $(this).data('chat-language')

      if (language === '' || chatLanguage === language) {
        $(this).show()
      } else {
        $(this).hide()
      }
    })
  }
})

$('#sortAscending').click(function () {
  const chatList = $('#chat-list')
  const chats = chatList.children('li').get()

  // Get the current sort order or default to 'asc'
  let sortOrder = $(this).data('sort-order') || 'asc'

  chats.sort(function (a, b) {
    const dateA = new Date($(a).data('date-created'))
    const dateB = new Date($(b).data('date-created'))
    let compareResult = dateA - dateB

    // Reverse the comparison result if the sort order is descending
    if (sortOrder === 'desc') {
      compareResult = -compareResult
    }

    return compareResult
  })

  chatList.empty() // clear existing LI elements

  $.each(chats, function (index, chat) {
    chatList.append(chat)
  })

  // Toggle the sort order for the next click
  if (sortOrder === 'asc') {
    $(this).data('sort-order', 'desc').text('Toggle Oldest to Newest Chats')
  } else {
    $(this).data('sort-order', 'asc').text('Toggle Newest to Oldest Chats')
  }
})
