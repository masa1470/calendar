function openMenu(cell) {
    const selectedDate = cell.getAttribute('data-date');
    const eventContent = cell.getAttribute('data-event'); // セルの予定内容を取得

    const menu = document.getElementById('event-menu');
    menu.style.display = 'block';
    menu.setAttribute('data-date', selectedDate);
    menu.setAttribute('data-event', eventContent); // メニューに予定内容を設定

    const rect = cell.getBoundingClientRect();
    menu.style.left = rect.left + 'px';
    menu.style.top = rect.top + window.scrollY + 'px';
}

// メニューを閉じる
function closeMenu() {
    document.getElementById('event-menu').style.display = 'none';
}

// 「追加」ボタンをクリックしたときに予定追加フォームを表示
function addEvent() {
    const date = document.getElementById('event-menu').getAttribute('data-date');
    document.getElementById('selected-date').value = date;
    document.getElementById('add-event-form').style.display = 'block';
    closeMenu();
}

// 「編集」ボタンをクリックしたときに予定編集フォームを表示
function editEvent() {
    const date = document.getElementById('event-menu').getAttribute('data-date');
    const eventContent = document.getElementById('event-menu').getAttribute('data-event');

    if (eventContent) {
        // フォームに既存の予定をセット
        document.getElementById('edit-date').value = date;
        document.getElementById('edit-event').value = eventContent;
        document.getElementById('edit-event-form').style.display = 'block';
    } else {
        alert("編集する予定がありません");
    }
    closeMenu();
}

// 編集フォームを閉じる
function closeEditForm() {
    document.getElementById('edit-event-form').style.display = 'none';
}


// 「削除」ボタンをクリックしたときにイベントを削除
function deleteEvent() {
    const menu = document.getElementById('event-menu');
    const date = menu.getAttribute('data-date'); // 選択された日付
    const eventContent = menu.getAttribute('data-event'); // 選択された予定の内容

    if (eventContent) {
        // 予定の内容を含めた確認メッセージ
        if (confirm(`${eventContent}」(${date})の予定を削除しますか？`)) {
            fetch(`/delete_event/${date}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            })
                .then(response => {
                    if (response.ok) {
                        alert("削除に成功しました");
                        location.reload(); // 削除後にページをリロードして最新情報を表示
                    } else {
                        alert("削除に失敗しました");
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert("削除中にエラーが発生しました");
                });
        }
    } else {
        alert("削除する予定が見つかりません");
    }
}

// フォームを閉じる
function closeForm() {
    document.getElementById('add-event-form').style.display = 'none';
}

// メニューを閉じる処理
window.onclick = function(event) {
    const form = document.getElementById('add-event-form');
    const menu = document.getElementById('event-menu');
    if (event.target == form || event.target == menu) {
        closeMenu();
    }
};
