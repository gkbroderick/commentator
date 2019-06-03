//POST Submission added via Button click to the `comment/` view handler.
// Handles new comments (commentId=0)
// and editing previously submitted comments.
function commentPost(event, elId) {
  event.preventDefault();
  var formEl = document.getElementById(elId);
  var playitemId = formEl.getAttribute('data-playitem-id');
  var playitemName = formEl.getAttribute('data-playitem-name');
  var playitemAirdate = formEl.getAttribute('data-playitem-airdate');
  var commentId = formEl.getAttribute('data-comment-id');
  var commentTextEl = formEl.querySelector('.comment-text');
  var helpText = formEl.querySelector('.help-text');

  //quick validation on textarea
  if (commentTextEl.value.trim().length < 1) {
    helpText.innerText = "Please enter a comment."
    return;
  }

  $.ajax({
    type: 'POST',
    url: 'comment/',
    data: {
      play_instance_kexp_id : playitemId,
      play_instance_name : playitemName,
      play_instance_airdate : playitemAirdate,
      comment_id : commentId,
      comment_text : commentTextEl.value,
    },
    success: function(data) {
      console.log(data.response, data.comment_time_edited);
      helpText.innerText = "";
      if (commentId <= 0) {
        //for new comments
        var counter = formEl.getAttribute('data-new-form-counter');
        commentTextEl.value = '';
        toggleFormVis('commentNewFormBtn' + counter, "commentCreator" + counter, "Create New Comment");
        addSubmittedComment(data.play_instance_kexp_id, playitemName, playitemAirdate, data.comment_id, data.comment_text, data.comment_time_edited);
      }
      else {
        //for edited comments
        document.getElementById('commentText' + commentId).innerText = data.comment_text;
        toggleFormVis('commentEditBtn' + commentId, "commentEditor" + commentId, "Edit Comment");
      }
    },
    error: function(jqXHR, errorString) {
      helpText.innerText = "An error has occured."
    }
  });
}

//Helper Function for hide/show comment submission form behavior
function toggleFormVis(buttonElId, formElId, initMessage) {
  var buttonEl = document.getElementById(buttonElId);
  var el = document.getElementById(formElId);
  el.classList.toggle("hide-form");
  if (buttonEl.getAttribute('data-interacted') == 'false') {
    buttonEl.innerText = "Cancel";
    buttonEl.setAttribute('data-interacted', 'true');
  }
  else {
    buttonEl.innerText = initMessage;
    buttonEl.setAttribute('data-interacted', 'false');
  }
}

//Quick and DOM-thrashy function to add new comments after submission success
function addSubmittedComment(playitemId, playitemName, playitemAirdate, commentId, commentText, commentDateCreated, csrfToken) {
  var elToAppend = document.getElementById("newCommentContainer" + playitemId);
  var el = document.createElement("div");
  var createdDate = new Date(commentDateCreated);
  var content ='<div id="comment'+ commentId +'" class="playlist-comment">';
  content +=  '<h6>'+ createdDate.toLocaleString('en-us',{month:'long', year:'numeric', day:'numeric', hour:'numeric', minute:'numeric'}) +'</h6>';
  content += '<p id="commentText' + commentId + '" class="comment-text">' + commentText + '</p>';
  content += '<button id="commentEditBtn'+ commentId + '" type="button" class="btn-box comment-btn" onClick="toggleFormVis(\'commentEditBtn'+ commentId + '\',\'commentEditor'+ commentId + '\', \'Edit Comment\')" data-interacted="false"> Edit Comment </button>';
  content += '<div id="commentEditor' + commentId + '" class="hide-form comment-submit-form" action="" method="post" data-playitem-id="' + playitemId + '" data-playitem-name="' + playitemName + '" data-playitem-airdate="' + playitemAirdate + '" data-comment-id="'+ commentId + '">';
  content += '<textarea class="comment-text" name="comment_text" rows="4" cols="60" maxlength="2000">' + commentText + '</textarea>'
  content += '<input type="button" class="btn-box comment-btn" value="Submit Comment Edit" onClick="commentPost(event, \'commentEditor'+ commentId + '\')"> <span class="help-text"></span></div></div>';

  el.innerHTML = content;
  elToAppend.appendChild(el);
}
