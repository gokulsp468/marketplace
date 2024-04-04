document.getElementsByName('tst').forEach(function(element) {
    element.addEventListener('click', function(event) {
        
		var elementsToHide = document.querySelectorAll('.tst');
		
		elementsToHide.forEach(function(elem) {
			elem.style.display = 'none';
		});
    });


	var hideTimeout = setTimeout(function() {
		var elementsToHide = document.querySelectorAll('.tst');
		elementsToHide.forEach(function(elem) {
			elem.style.display = 'none';
		});
	}, 5000);})