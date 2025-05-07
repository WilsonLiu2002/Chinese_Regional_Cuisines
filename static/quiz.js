$(function() {

  let timerId;

  // --- Timer for drag & drop (if present) ---
  if ($('.draggable[data-correct]').length) {
    // insert a wrapper for timer + restart button
    $('<div id="timer-wrapper"><span id="timer">1:00</span></div>')
      .insertBefore('.drag-container:first');

    let remaining = 60;
    const $timer = $('#timer');

    timerId = setInterval(function() {
      remaining--;
      const m = Math.floor(remaining / 60);
      const s = remaining % 60;
      $timer.text(m + ':' + (s < 10 ? '0' : '') + s);

      if (remaining <= 0) {
        clearInterval(timerId);
        $timer.text('0:00').addClass('time-up');
        // disable further dragging
        $('.draggable').attr('draggable', false).css('cursor', 'default');
        $('#bowl-container').off('dragover drop');

        // if quiz not complete, show restart button next to the timer
        const correctCount = $('.draggable[data-correct="true"]').length;
        const placedCount  = $('#bowl img').length;
        if (placedCount < correctCount && !$('#restart-btn').length) {
          $('#timer-wrapper').append(
            '<button id="restart-btn">Restart Quiz</button>'
          );
          $('#restart-btn').on('click', () => location.reload());
        }
      }
    }, 1000);
  }

  // --- Drag & Drop Logic ---
  let placed = 0;
  const correctCount = $('.draggable[data-correct="true"]').length;

  $('.draggable')
    .on('dragstart', function(e) {
      e.originalEvent.dataTransfer
        .setData('text/plain', $(this).data('correct'));
      $(this).addClass('dragging');
    })
    .on('dragend', function() {
      $(this).removeClass('dragging');
    });

  $('#bowl-container')
    .on('dragover', e => e.preventDefault())
    .on('drop', function(e) {
      e.preventDefault();
      const isCorrect = e.originalEvent.dataTransfer
                            .getData('text/plain') === 'true';
      const $img = $('.dragging');

      if (!isCorrect) {
        $img.css('border-color', 'red');
        setTimeout(() => $img.css('border-color', ''), 300);
        return;
      }
      if ($img.data('placed')) return;

      $img.data('placed', true);
      placed++;
      const $clone = $img.clone()
                         .removeClass('dragging')
                         .removeAttr('draggable');
      $('#bowl').append($clone);

      if (placed === correctCount) {
        $('#message').css('visibility', 'visible');
        // stop the timer on success
        clearInterval(timerId);
        
        $('.cook-btn').show();

        $('.cook-btn').off('click').on('click', function() {
          const qid = this.id.replace('cook-btn-','');
          const $overlay = $('#cook-overlay-' + qid);
          $overlay.show();

          // hide when overlay itself is clicked
          $overlay.off('click').on('click', function() {
            $(this).hide();
          });
        });
      }
    });
  
    // --- Multiple Choice Logic with Feedback ---
    $(document).ready(function () {
      $('.check-answer').click(function () {
        const $form     = $(this).closest('.mcq-form');
        const mpId      = $form.data('mp-id');
        const correct   = $form.data('answer');
        const $inputs   = $form.find('input[type=radio]');
        const pickedVal = $inputs.filter(':checked').val();
        const $fb       = $form.find('.mcq-feedback');
        const $learnBtn = $form.find('.learn-to-cook-btn');
        const region    = $form.closest('.quiz-container').data('region');
    
        if (!pickedVal) {
          $learnBtn.hide();
          return $fb.text('Please select one.').css('color', 'orange');
        }
    
        // Get letter A/B/C/D for feedback lookup
        const idx    = $inputs.index($inputs.filter(':checked'));
        const letter = String.fromCharCode(65 + idx);
        const mpFeed = (FEEDBACK_DATA[mpId] || {})[letter];
        const isCorrect = pickedVal === correct;
    
        // Display feedback
        if (mpFeed) {
          const prefix = isCorrect ? '✅ ' : '❌ ';
          $fb.text(prefix + mpFeed).css('color', isCorrect ? 'green' : 'red');
        } else {
          if (isCorrect) {
            $fb.text('✅ Correct!').css('color', 'green');
          } else {
            $fb.text(`❌ Nope, the answer is "${correct}".`).css('color', 'red');
          }
        }
    
        // Show Learn to Cook button with correct link
        const $label    = $inputs.filter(':checked').closest('label.option');
        const dishValue = $inputs.filter(':checked').val();
    
        if (region && dishValue) {
          const link = `/learn/${region}/${dishValue}`;
          $learnBtn
            .off('click')
            .on('click', () => window.location.href = link)
            .show();
        } else {
          $learnBtn.hide();
        }
      });
    });     
});  