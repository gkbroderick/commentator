//Submission
$('.comment-submit-form').submit(function(){
  var playitemId = this.getAttribute('data-playitem-id');
  var playitemName = this.getAttribute('data-playitem-name');
  var playitemAirdate = this.getAttribute('data-playitem-airdate');
  var commentId = this.getAttribute('data-comment-id');

  var formEl = event.target;
  var commentTextEl = formEl.querySelector('.comment-text');

  // todo, quick form validation, help text

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
      //for new comments
      if (commentId <= 0) {
        var counter = formEl.getAttribute('data-new-form-counter');
        var csrfToken = formEl.querySelector('input');
        commentTextEl.value = '';
        toggleFormVis('commentNewFormBtn' + counter, "commentCreator" + counter, "Create New Comment");
        addSubmittedComment(data.play_instance_kexp_id, playitemName, playitemAirdate, data.comment_id, data.comment_text, data.comment_time_edited, csrfToken);
      }
      else {
        document.getElementById('commentText' + commentId).innerText = data.comment_text;
        toggleFormVis('commentEditBtn' + commentId, "commentEditor" + commentId, "Edit Comment");
      }


    },
    error: function(jqXHR, errorString) {
      console.log('errorString');
    }
  });
  return false;
})

//Helper Functions for hide/show buttons and adding new comments to DOM

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


function addSubmittedComment(playitemId, playitemName, playitemAirdate, commentId, commentText, commentDateCreated, csrfToken) {
  var elToAppend = document.getElementById("newCommentContainer" + playitemId);
  var el = document.createElement("div");
  var createdDate = new Date(commentDateCreated);
  var content ='<div id="comment'+ commentId +'" class="playlist-comment">';
  content +=  '<h6>'+ createdDate.toLocaleString('en-us',{month:'long', year:'numeric', day:'numeric', hour:'numeric', minute:'numeric'}) +'</h6>';
  content += '<p id="commentText+ ' + commentId + '">' + commentText + '</p></div>';
  content += '<button id="commentEditBtn'+ commentId + '" type="button" class="btn-box" onClick="toggleFormVis(\'commentEditBtn'+ commentId + '\',\'commentEditor'+ commentId + '\', \'Edit Comment\')" data-interacted="false"> Edit Comment </button>';
  content += '<form id="commentEditor' + commentId + '" class="hide-form comment-submit-form" action="" method="post" data-playitem-id="' + playitemId + '" data-playitem-name="' + playitemName + '" data-playitem-airdate="' + playitemAirdate + '" data-comment-id="'+ commentId + '">';
  content += '<textarea class="comment-text" name="comment_text" rows="4" cols="60" maxlength="2000">' + commentText + '</textarea> <input type="submit" class="btn-box" value="Submit Edited Comment"> <span class="help-text"></span></form>';

  el.innerHTML = content;
  elToAppend.appendChild(el);
  //add CSRF Token
  document.getElementById('commentEditor' + commentId).prepend(csrfToken);
}
