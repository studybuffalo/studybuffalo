function CheckNotificationPermissions() {
  let permission = false;

  // Check for notification support
  if (!('Notification' in window)) {
    console.warn('Notifications not supported');

  // Notification privileges granted
  } else if (Notification.permission === 'granted') {
    permission = true;

  // Request notification privileges
  } else if (Notification.permission !== 'denied') {
    Notification.requestPermission((perm) => {
      if (perm === 'granted') {
        permission = true;
      }
    });
  // Otherwise, notification permissions denied
  } else {
    console.log('Notifications denied by user');
  }

  return permission;
}

function SendMessage(msg, tag) {
  const permission = CheckNotificationPermissions;

  if (permission) {
    // Get details of the message
    const title = 'Study Buffalo Substitutions App';
    const options = {
      body: msg,
      icon: '/static/images/android-chrome-192x192.png',
      tag,
    };

    Notification(title, options);
  }
}

function SearchText(button) {
  // Get the editable div to retrieve the search query
  const $button = $(button);
  const $parentDiv = $button.parent();
  const $content = $parentDiv.children('.word');

  // Open a new window with the search
  window.open(`https://google.com/search?q=${$content.text()}`);
}

function ShowSource(button) {
  // Get the editable div to retrieve the source text
  const $button = $(button);
  const $parentDiv = $button.parent();
  const $content = $parentDiv.children('.word');

  // Open a new window with the search
  alert($content.attr('data-original'));
}

function CreateWordInputs(data) {
  const $div = $('<div></div>');

  // Create the Language select
  const $languageSelect = $(sessionStorage.getItem('language_select'));
  $languageSelect
    .val(data.language)
    .appendTo($div);

  // Create the Dictionary Type select
  const $dictionaryTypeSelect = $(
    sessionStorage.getItem('dictionary_type_select'),
  );
  $dictionaryTypeSelect
    .val(data.dictionary_type)
    .appendTo($div);

  // Create the Dictionary Class select
  const $dictionaryClassSelect = $(
    sessionStorage.getItem('dictionary_class_select'),
  );

  $dictionaryClassSelect
    .val(data.dictionary_class)
    .appendTo($div);

  // Create an editable div to hold the word
  const $input = $('<div></div>');
  $input
    .attr('contenteditable', 'true')
    .attr('data-original', data.original)
    .addClass('word')
    .text(data.word)
    .appendTo($div);

  // Create a search button
  const $googleButton = $('<button></button>');
  $googleButton
    .addClass('google')
    .on('click', () => {
      SearchText(this);
    })
    .appendTo($div);

  const $googleSpan = $('<span></span>');
  $googleSpan
    .text('Search')
    .appendTo($googleButton);

  // Create a show original button
  const $originalButton = $('<button></button>');
  $originalButton
    .addClass('source')
    .on('click', () => {
      ShowSource(this);
    })
    .appendTo($div);

  const $originalSpan = $('<span></span>');
  $originalSpan
    .text('Source')
    .appendTo($originalButton);

  return $div;
}

function RemovePendingWord(pendingID) {
  // Setup CSRF token for POST
  const CSRF = $('[name=csrfmiddlewaretoken]').val();

  $.ajaxSetup({
    beforeSend: (xhr, settings) => {
      if (!this.crossDomain) {
        xhr.setRequestHeader('X-CSRFToken', CSRF);
      }
    },
  });

  $.ajax({
    url: 'delete-pending-word/',
    data: {
      pending_id: pendingID,
    },
    type: 'POST',
    success: (results) => {
      if (results.success) {
        // Remove this entry form the page
        $(`#pending-${results.id}`).remove();

        // Reduce the pending count by 1
        const $count = $('#word_count');
        $count.text(Number($count.text()) - 1);

        // Request to display additional entries
        RetrieveEntries();
      }

      SendMessage(results.message, 'delete-pending');
    },
    error: (jqXHR, textStatus, errorThrown) => {
      SendMessage(
        `Error deleting entry - ${textStatus}: ${errorThrown}`,
        'error',
      );
    },
  });
}

function AddWord(button, e) {
  const { modelName } = e;
  const messageTag = modelName === 'word' ? 'new-word' : 'new-excluded-word';
  const $entry = $(button).parents('.entry');

  // Get the ID of the entry in the pending model
  const pendingID = $entry.attr('data-id');

  // Get the word element
  const $word = $entry.find('.word');

  // Get the word text
  const word = $word.text();

  // Get the language of the word
  const language = $entry.find('.language').val();

  // Get the dictionary type of the word
  const dictionaryType = $entry.find('.dictionary-type').val();

  // Get the dictionary class of the word
  const dictionaryClass = $entry.find('.dictionary-class').val();

  // Get the add and exclude buttons
  const addButton = $entry.find('.add')[0];
  const excludeButton = $entry.find('.exclude')[0];

  $.ajax({
    url: 'add-new-word/',
    data: {
      pendingID,
      modelName,
      word,
      language,
      dictionaryType,
      dictionaryClass,
    },
    type: 'POST',
    beforeSend: (jqXHR, settings) => {
      // Setup the CSRF token for the POST request
      if (!this.crossDomain) {
        const CSRF = $('[name=csrfmiddlewaretoken]').val();

        jqXHR.setRequestHeader('X-CSRFToken', CSRF);
      }

      // Disable add/exclude buttons to prevent duplicate POSTs
      addButton.disabled = true;
      excludeButton.disabled = true;
    },
    success: (results) => {
      if (results.success) {
        RemovePendingWord(results.id);
      }

      SendMessage(results.message, messageTag);
    },
    error: (jqXHR, textStatus, errorThrown) => {
      SendMessage(
        `Error adding entry - ${textStatus}: ${errorThrown}`,
        'error',
      );

      // Re-enable buttons to allow re-send
      addButton.disabled = false;
      excludeButton.disabled = false;
    },
  });
}

function DeleteWord(button) {
  const pendingID = $(button).parents('.entry').attr('data-id');

  RemovePendingWord(pendingID);
}

function CreateEntryDOM(entry) {
  const $entryDiv = $('<div></div>');
  $entryDiv
    .addClass('entry')
    .attr('id', `pending-${entry.id}`)
    .attr('data-id', entry.id)
    .appendTo($('#entries'));

  // Create the word div
  const $wordDiv = CreateWordInputs(entry);
  $wordDiv
    .addClass('word-div')
    .appendTo($entryDiv);

  // Create the other options
  const $otherDiv = $('<div></div>');
  $otherDiv
    .addClass('other')
    .appendTo($entryDiv);

  // Create button to add word to dictionary
  const $addButton = $('<button></button>');
  $addButton
    .addClass('add')
    .on('click', () => {
      AddWord(this, { modelName: 'word' });
    })
    .appendTo($otherDiv);

  const $addSpan = $('<span></span>');
  $addSpan
    .text('Add')
    .appendTo($addButton);

  // Create a button to exclude entries from the dictionary
  const $excludeButton = $('<button></button>');
  $excludeButton
    .addClass('exclude')
    .on('click', () => {
      AddWord(this, { modelName: 'excluded' });
    })
    .appendTo($otherDiv);

  const $excludeSpan = $('<span></span>');
  $excludeSpan
    .text('Exclude')
    .appendTo($excludeButton);

  // Create button to delete pending word
  const $deleteButton = $('<button></button>');
  $deleteButton
    .addClass('delete')
    .on('click', () => { DeleteWord(this); })
    .appendTo($otherDiv);

  const $deleteSpan = $('<span></span>');
  $deleteSpan
    .text('Delete')
    .appendTo($deleteButton);
}

function UpdateEntries(results) {
  $.each(results, (id, entry) => {
    CreateEntryDOM(entry);
  });
}

function RetrieveEntries() {
  const $entries = $('.entry');

  // Calculate how many entries to retrieve
  const maxEntries = Number($('#entries-to-display').val());
  const currentNum = $entries.length;
  const requestNum = maxEntries > currentNum ? maxEntries - currentNum : 0;

  // Calculate the last ID retrieved
  let lastNum = 0;

  if ($entries.length) {
    lastNum = $entries.last().attr('data-id');
  }

  // Setup CSRF token for POST
  const CSRF = $('[name=csrfmiddlewaretoken]').val();

  $.ajaxSetup({
    beforeSend: (xhr, settings) => {
      if (!this.crossDomain) {
        xhr.setRequestHeader('X-CSRFToken', CSRF);
      }
    },
  });

  $.ajax({
    url: 'retrieve-entries/',
    data: {
      last_id: lastNum,
      request_num: requestNum,
    },
    type: 'POST',
    success: (results) => {
      UpdateEntries(results.content);
    },
    error: (jqXHR, textStatus, errorThrown) => {
      console.error('Error retrieving entries');
      console.error(`${textStatus}: ${errorThrown}`);
    },
  });
}

function ExcludeWord(button) {
  console.log('Excluding word stuff goes here');
}

function ClearDisplayedEntries() {
  $('#entries').empty();
}

function SaveSelectData(selectData) {
  sessionStorage.setItem('language_select', selectData.language);
  sessionStorage.setItem('dictionary_type_select', selectData.dict_type);
  sessionStorage.setItem('dictionary_class_select', selectData.dict_class);
}

function InitiateInitialLoad() {
  $.ajax({
    url: 'retrieve-select-data/',
    data: {},
    type: 'GET',
    success: (results) => {
      // Save the data for the select inputs
      SaveSelectData(results);

      // Retrieve the initial pending entries
      RetrieveEntries();
    },
    error: (jqXHR, textStatus, errorThrown) => {
      console.error('Error retrieving entries');
      console.error(`${textStatus}: ${errorThrown}`);
    },
  });
}

$(document).ready(() => {
  // Store database input data and fetch initial query results
  InitiateInitialLoad();

  // Add event listener to update nubmer of queries
  $('#options').on('change', () => {
    ClearDisplayedEntries();
    RetrieveEntries();
  });
});
