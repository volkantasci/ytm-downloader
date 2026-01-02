# Uygulama Hakkında

Basit bir Python projesi yapıyoruz. Amacımız: music.youtube.com üzerinden alınmış sanatçı linklerini kullanarak, albümlerin tümünü indirip, navidrome için uygun bir formatta organize etmek. Dolayısıyla bir music klasörü oluşturacağız. Bu klasörün içinde albümler olacak. Her albüm klasörü içinde albümün tüm şarkıları olacak. Her şarkı klasörü içinde ilgili müzik dosyası ve albüm kapağı yer almalı. İlgili albüm kapağı ilgili albümdeki her müziğe metadata olarak işlenmeli. Bunun için ffmpeg kullanılabilir. Elbette performans için çoklu process kullanacağız. 

# Şimdi Tamamlanması Gerekenler

1. Şarkıları indirmekte hiçbir sorunumuz yok ancak albümleri ayırmada ve sanatçı isimlerini ayırmada hatalar var. Örneğin bazı parçalarda 3 sanatçı var görübüyor ama üç sanatçı ismi de aynı. Örneğin "Oğuz Aksaç, Oğuz Aksaç, Oğuz Aksaç" gibi. Öte yandan Albüm ismi aynı olup birden çok albüm çıkıyor ortaya. Örneğin Mustafa Özarslan'a ait Beyhude albümü çok defa tekrar ediyor. İçindeki şarkı farklı ama albüm adı aynı. Bu tür problemleri de düzeltmemiz gerekiyor. 