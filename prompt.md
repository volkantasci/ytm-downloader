# Uygulama Hakkında

Basit bir Python projesi yapıyoruz. Amacımız: music.youtube.com üzerinden alınmış sanatçı linklerini kullanarak, albümlerin tümünü indirip, navidrome için uygun bir formatta organize etmek. Dolayısıyla bir music klasörü oluşturacağız. Bu klasörün içinde albümler olacak. Her albüm klasörü içinde albümün tüm şarkıları olacak. Her şarkı klasörü içinde ilgili müzik dosyası ve albüm kapağı yer almalı. İlgili albüm kapağı ilgili albümdeki her müziğe metadata olarak işlenmeli. Bunun için ffmpeg kullanılabilir. Elbette performans için çoklu process kullanacağız. 

# Şimdi Tamamlanması Gerekenler

1. Şu anda tüm albümler yakalanmıyor. Belki de headless modda bir tarayıcı açmak gerekir. Böylece albüm kapağı linki, albüm şarkıları linki gibi bilgileri alabiliriz. Bunun için selenium kullanabiliriz. Gereken yapıyı profesyonel bir şekilde oluşturmalısınız. 