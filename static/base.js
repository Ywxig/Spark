function sendPing() {
            fetch('/api/ping', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                keepalive: true // Помогает отправить финальный пинг при уходе
            }).catch(err => console.log("Сервер недоступен"));
        }

        // Отправляем пинг сразу при загрузке страницы
        sendPing();

        // И затем каждые 1.5 секунды
        setInterval(sendPing, 1500);

        // Дополнительно: отправляем пинг прямо в момент закрытия/перехода,
        // чтобы перестраховаться и продлить серверу жизнь на время загрузки новой страницы
        window.addEventListener('beforeunload', () => {
            sendPing();
        });