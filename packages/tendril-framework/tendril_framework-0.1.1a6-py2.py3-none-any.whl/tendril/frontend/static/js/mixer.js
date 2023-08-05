/*!
 * MixItUp based object filtering and sorting
 * Based heavily on the pen by patrickkunka at
 * http://codepen.io/patrickkunka/pen/KpVPWo
 *
 * Released under the MIT license
 *
 * Copyright 2016 Chintalagiri Shashank.
 *
 */


// To keep our code clean and modular, all custom functionality will be
// contained inside a single object literal called "multiFilter".

var multiFilter = {

  // Declare any variables we will need as properties of the object

  $filterGroups: null,
  $filterUi: null,
  $reset: null,
  groups: [],
  sorts: [],
  outputArray: [],
  outputString: '',

  // The "init" method will run on document ready and cache any jQuery
  // objects we will need.

  init: function(){
    // As a best practice, in each method we will asign "this" to the
    // variable "self" so that it remains scope-agnostic. We will use
    // it to refer to the parent "checkboxFilter" object so that we
    // can share methods and properties between all parts of the object.
    var self = this;

    self.$filterUi = $('#filters');
    self.$filterGroups = $('.filter-group');
    self.$filterButtons = $('.filter');
    self.$sortGroups = $('.sort-group');
    self.$sortButtons = $('.sort');
    self.$reset = $('#reset');
    self.$container = $('#card-container');

    self.$filterGroups.each(function(){
      self.groups.push({
        $inputs: $(this).find('input'),
        $buttons: $(this).find('.filter'),
        active: [],
		tracker: false
      });
    });

    self.$sortGroups.each(function(){
        self.sorts.push({
            $buttons: $(this).find('.sort'),
            active: []
        });
    });

    self.bindHandlers();
  },

  // The "bindHandlers" method will listen for whenever a form value changes.

  bindHandlers: function(){
    var self = this,
        typingDelay = 300,
        typingTimeout = -1,
        resetTimer = function() {
          clearTimeout(typingTimeout);

          typingTimeout = setTimeout(function() {
            self.parseFilters();
          }, typingDelay);
        };

    self.$filterButtons
      .filter('a')
    	.on('click', function() {
            if(this.getAttribute('data-filter') == 'all'){
                if(!$(this).hasClass('active')){
                    $(this).parent().siblings().each( function(){
                        $(this).children()
                        .removeClass('active');
                    });
                    $(this).addClass('active');
                }
            }
            else{
                if(!$(this).hasClass('active')){
                    $(this).parent().parent()
                        .find('a[data-filter="all"]')
                        .removeClass('active');
                    $(this).addClass('active');
                }
                else{
                    $(this).removeClass('active');
                    if (!$(this).parent().parent().find('a.active').length){
                        $(this).parent().parent()
                            .find('a[data-filter="all"]')
                            .addClass('active');
                    }
                }
            }

            self.parseFilters();
    	});

    self.$sortButtons
        .filter('a')
        .on('click', function(){
            if(!$(this).hasClass('active')){
//                $(this).parent().siblings().each( function(){
//                    $(this).children()
//                    .removeClass('active');
//                });
                self.$sortButtons.filter('a')
                    .removeClass('active');
                $(this).addClass('active');
            }
            else{
                $(this).removeClass('active');
            }
            self.parseSorts();
        });

    self.$filterGroups
      .filter('.search')
      .on('keyup change', resetTimer);

    self.$reset.on('click', function(e){
      e.preventDefault();
      self.$filterUi[0].reset();
      self.$filterButtons
        .filter('a')
        .removeClass('active');
      self.$sortButtons
        .filter('a')
        .removeClass('active');
      self.$filterButtons
        .filter('a[data-filter="all"]')
        .addClass('active');
      self.$filterUi.find('input[type="text"]').val('');
      self.parseFilters();
      self.parseSorts();
    });
  },

  parseSorts: function(){
    var self = this,
        sortstring = '';

    if (self.$sortButtons.filter('a.active').length){
        self.$sortButtons
            .filter('a.active').each(function(){
                sortstring = this.getAttribute('data-sort');
            });
    }
    else{
        sortstring = 'default';
    }

    if(self.$container.mixItUp('isLoaded')){
    	self.$container.mixItUp('sort', sortstring);
    }
  },

  // The parseFilters method checks which filters are active in each group:
  parseFilters: function(){
    var self = this;
    // loop through each filter group and add active filters to arrays

    for(var i = 0, group; group = self.groups[i]; i++){
      group.active = []; // reset arrays
      var all = [],
          sendall = 0;

      group.$inputs.each(function(){
        var searchTerm = '',
       		$input = $(this),
            minimumLength = 2;

        if ($input.is('[type="text"]') && this.value.length >= minimumLength) {
          searchTerm = this.value
            .trim()
            .toLowerCase()
            .replace(' ', '-');

          group.active[0] = '[data-title*=' + searchTerm + ']';
        }
      });

      group.$buttons.each(function(){
        var fstring = this.getAttribute('data-filter');
        if(!(fstring == 'all')){
            all.push(fstring);
            if($(this).hasClass('active')){
                group.active.push(fstring);
            }
        }
        else{
            if($(this).hasClass('active')){
                sendall = 1;
            }
        }
      });

      if (sendall){
        group.active = all;
      }
      group.active.length && (group.tracker = 0);
    }

    self.concatenate();
  },

  // The "concatenate" method will crawl through each group, concatenating filters as desired:

  concatenate: function(){
    var self = this,
		  cache = '',
		  crawled = false,
		  checkTrackers = function(){
        var done = 0;

        for(var i = 0, group; group = self.groups[i]; i++){
          (group.tracker === false) && done++;
        }

        return (done < self.groups.length);
      },
      crawl = function(){
        for(var i = 0, group; group = self.groups[i]; i++){
          group.active[group.tracker] && (cache += group.active[group.tracker]);

          if(i === self.groups.length - 1){
            self.outputArray.push(cache);
            cache = '';
            updateTrackers();
          }
        }
      },
      updateTrackers = function(){
        for(var i = self.groups.length - 1; i > -1; i--){
          var group = self.groups[i];

          if(group.active[group.tracker + 1]){
            group.tracker++;
            break;
          } else if(i > 0){
            group.tracker && (group.tracker = 0);
          } else {
            crawled = true;
          }
        }
      };

    self.outputArray = []; // reset output array

	  do{
		  crawl();
	  }
	  while(!crawled && checkTrackers());

    self.outputString = self.outputArray.join();

    // If the output string is empty, show all rather than none:

    !self.outputString.length && (self.outputString = 'all');

    // console.log(self.outputString);

    // ^ we can check the console here to take a look at the filter string that is produced

    // Send the output string to MixItUp via the 'filter' method:

	  if(self.$container.mixItUp('isLoaded')){
    	self.$container.mixItUp('filter', self.outputString);
	  }
  }
};

// On document ready, initialise our code.

$(function(){

  // Initialize multiFilter code

  multiFilter.init();

  // Instantiate MixItUp

  $('#card-container').mixItUp({
    controls: {
      enable: false // we won't be needing these
    },
    selectors:{
      target: '.card-instance'
    },
    animation: {
      easing: 'cubic-bezier(0.86, 0, 0.07, 1)',
      queueLimit: 3,
      duration: 600
    },
    callbacks: {
		onMixEnd: function(state){
		    target = document.getElementById("filter-status");
		    msg = "Showing <b>" + state.totalShow.toString();
		    msg += "</b> of " + state.totalTargets.toString() + " ";
		    msg += target.getAttribute('data-note');
			target.innerHTML = msg;
			target.style.display = 'block';
		}
	}
  });
});
