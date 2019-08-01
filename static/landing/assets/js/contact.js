
		document.querySelector('.contactsuccess').addEventListener('click', function (e) {
        e.preventDefault();
        // UI ELEMENTS
        const name = document.querySelector('#name');
        const email = document.querySelector('#email');
        const url = document.querySelector('#url');
        const message = document.querySelector('#message');
		
		const ck = [name,email,url,message]
		var a = 0;
		ck.forEach(item => {
			item.style.border = '2px solid green';
			if(item.value === ''){
				a++;
				item.style.border = '2px solid red';
			}
		});
			
        const sendBtn = document.querySelector('.contactsuccess');
        const msg = document.querySelector('.success-msg');
		 const loader = document.querySelector('.sending-gif');

        //   Clear Fields
        function clear() {
            name.value = '';
            email.value = '';
            url.value = '';
            message.value = '';
        }

        
		if(a === 0){
		//   Loader On, Button Disabled
        loader.style.display = 'block';
			
        sendBtn.disabled = true;
        $.ajax({
                url: 'mail.php',
                method: 'POST',
                data: {
                    name: name.value,
                    email: email.value,
                    url: url.value,
                    message: message.value
                }
            })
            .done(function (response) {
                console.log(response);
                setTimeout(() => {
                    loader.style.display = 'none';
                    msg.style.display = 'block';
                    setTimeout(() => {
                        msg.style.display = 'none';
                        sendBtn.disabled = false;
                        clear();
						ck.forEach(item => item.style.border = 'none');
                    }, 1000);
                }, 1500);
            })
            .error(function () {
                console.log('ERROR');
            });
		}
    });