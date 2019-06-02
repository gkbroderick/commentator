//Submission
$('.comment-submit-form').submit(function(){
  var playitemId = this.getAttribute('data-playitem-id');
  var playitemName = this.getAttribute('data-playitem-name');
  var playitemAirdate = this.getAttribute('data-playitem-airdate');
  var commentId = this.getAttribute('data-comment-id');

  var formEl = event.target;
  var commentTextEl = formEl.querySelector('.comment-text');
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
      console.log(data.response);
      commentTextEl.value = '';
    },
    // error: function(jqXHR, errorString) {
    //   console.log('errorString');
    // }
  });
  return false;
})

//Helper Functions for hide/show buttons and adding new comments to DOM
