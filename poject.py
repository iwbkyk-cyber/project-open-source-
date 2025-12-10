<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Profile Card — Step 3</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" />
  <style>
    /* 2단계 스타일 유지 + 약간 정리 */
    body{font-family:Pretendard,system-ui;margin:24px;background:#f7fafc;color:#0f1724}
    .wrap{max-width:760px;margin:0 auto}
    .panel{background:#fff;padding:18px;border-radius:12px;box-shadow:0 8px 20px rgba(2,6,23,0.06);margin-bottom:14px}
    .color-grid{display:flex;gap:8px;margin:8px 0}
    .swatch{width:36px;height:36px;border-radius:50%;cursor:pointer;border:2px solid #fff;box-shadow:0 2px 6px rgba(0,0,0,0.08)}
    .swatch.active{transform:scale(1.05);border-color:#111}
    .id-card{padding:20px;border-radius:12px}
    .avatar-box{width:80px;height:80px;border-radius:12px;background:#e6eef8;margin:0 auto 8px;display:flex;align-items:center;justify-content:center}
    #previewThumb{display:block;width:64px;height:64px;object-fit:cover;border-radius:8px;margin-top:8px}
    .tags{display:flex;gap:6px;justify-content:center;margin-top:8px}
    .tag{background:#fff;padding:6px 10px;border-radius:20px;border:1px solid #e6eef8;font-size:13px}
    .hidden{display:none}
  </style>
</head>
<body>
  <div class="wrap">
    <section id="viewForm" class="panel">
      <h2 style="text-align:center; margin-top:0">프로필 생성기</h2>
      <form id="profileForm">
        <label>이름</label>
        <input type="text" id="name" placeholder="닉네임 입력" required>
        <label>프로필 사진</label>
        <input type="file" id="profileImg" accept="image/*">
        <img id="previewThumb" class="hidden" alt="썸네일">
        <label>카드 색상</label>
        <div class="color-grid">
          <div class="swatch bg-ocean active" data-theme="bg-ocean" style="background:linear-gradient(135deg,#e0f2fe,#bae6fd)"></div>
          <div class="swatch bg-peach" data-theme="bg-peach" style="background:linear-gradient(135deg,#ffe4e6,#fda4af)"></div>
          <div class="swatch bg-mint" data-theme="bg-mint" style="background:linear-gradient(135deg,#dcfce7,#86efac)"></div>
          <div class="swatch bg-indigo" data-theme="bg-indigo" style="background:linear-gradient(135deg,#e0e7ff,#a5b4fc)"></div>
        </div>
        <label>MBTI</label>
        <div style="display:flex; gap:5px">
          <input type="text" id="mbti" placeholder="ENFP">
          <button type="button" id="randomMbtiBtn" style="width:60px;">랜덤</button>
        </div>
        <label>좋아하는 음식</label>
        <input type="text" id="food" placeholder="떡볶이">
        <label>취미</label>
        <input type="text" id="hobby" placeholder="누워있기">
        <label>연락 선호 시간</label>
        <select id="contactTime">
          <option value="any">상관없음</option>
          <option value="day">낮</option>
          <option value="night">밤</option>
        </select>
        <label>문체</label>
        <select id="tone">
          <option value="casual">친근하게</option>
          <option value="polite">공손하게</option>
        </select>
        <button type="submit" class="btn-main">완료 ✨</button>
      </form>
    </section>

    <section id="viewResult" class="panel hidden">
      <div id="captureTarget">
        <div class="id-card bg-ocean" id="cardEl">
          <div class="avatar-box" id="rAvatar"></div>
          <h2 id="rName">이름</h2>
          <span id="rMbti">MBTI</span>
          <div class="tags" id="rTags"></div>
          <div id="rDesc"></div>
        </div>
      </div>
      <div class="actions">
        <button id="copyBtn" class="btn-sub">텍스트 복사</button>
        <button id="downloadBtn" class="btn-sub download">이미지 저장</button>
      </div>
      <button id="backBtn" class="back-btn">다시 만들기</button>
    </section>
  </div>

  <script>
    // 데이터 뱅크 (랜덤용)
    const mbtiList = ["ENFP","INFP","INFJ","INTJ","ISTJ","ISFJ","ESTP","ESFP","ENTP","ENTJ"];

    // 색상 스와치 & 미리보기
    const swatches = document.querySelectorAll(".swatch");
    const cardEl = document.getElementById("cardEl");
    const profileImg = document.getElementById("profileImg");
    const previewThumb = document.getElementById("previewThumb");

    swatches.forEach(s => {
      s.addEventListener("click", () => {
        document.querySelector(".swatch.active")?.classList.remove("active");
        s.classList.add("active");
        const theme = s.dataset.theme;
        cardEl.className = "id-card " + theme;
      });
    });

    // 이미지 업로드 → 폼 썸네일 및 결과 아바타용 데이터 저장
    let avatarSrc = "";
    profileImg.addEventListener("change", (e) => {
      const file = e.target.files[0];
      if (!file) { previewThumb.classList.add("hidden"); avatarSrc = ""; return; }
      const reader = new FileReader();
      reader.onload = (evt) => {
        previewThumb.src = evt.target.result;
        previewThumb.classList.remove("hidden");
        avatarSrc = evt.target.result; // 결과에서 사용
      };
      reader.readAsDataURL(file);
    });

    // MBTI 랜덤
    document.getElementById("randomMbtiBtn").addEventListener("click", () => {
      const pick = mbtiList[Math.floor(Math.random() * mbtiList.length)];
      document.getElementById("mbti").value = pick;
    });

    // 설명 생성 (간단)
    function makeDesc(name, food, hobby, tone, contact) {
      const contactText = contact === "day" ? "낮 연락 선호." : contact === "night" ? "밤 연락 선호." : "연락 시간 상관없음.";
      if (tone === "casual") {
        return `안녕, 나는 ${name}. ${food} 좋아하고 ${hobby} 하는 걸 즐겨. ${contactText}`;
      } else {
        return `안녕하세요, ${name}입니다. ${food}을 좋아하며 ${hobby}을(를) 즐깁니다. ${contactText}`;
      }
    }

    // 폼 제출 → 결과 반영
    document.getElementById("profileForm").addEventListener("submit", (e) => {
      e.preventDefault();
      const name = document.getElementById("name").value.trim();
      const mbti = document.getElementById("mbti").value.trim();
      const food = document.getElementById("food").value.trim() || "음식";
      const hobby = document.getElementById("hobby").value.trim() || "취미";
      const tone = document.getElementById("tone").value;
      const contact = document.getElementById("contactTime").value;

      // 결과에 반영
      document.getElementById("rName").textContent = name || "이름 없음";
      document.getElementById("rMbti").textContent = mbti || "MBTI 없음";

      // 아바타
      const rAvatar = document.getElementById("rAvatar");
      rAvatar.innerHTML = "";
      if (avatarSrc) {
        const img = document.createElement("img");
        img.src = avatarSrc;
        img.style.width = "100%";
        img.style.height = "100%";
        img.style.objectFit = "cover";
        rAvatar.appendChild(img);
      } else {
        rAvatar.textContent = name ? name.charAt(0) : "?";
      }

      // 태그
      const tagsEl = document.getElementById("rTags");
      tagsEl.innerHTML = "";
      const tag1 = document.createElement("div"); tag1.className="tag"; tag1.textContent = "#" + food;
      const tag2 = document.createElement("div"); tag2.className="tag"; tag2.textContent = "#" + hobby;
      tagsEl.appendChild(tag1); tagsEl.appendChild(tag2);

      // 소개문
      document.getElementById("rDesc").textContent = makeDesc(name, food, hobby, tone, contact);

      // 화면 전환
      document.getElementById("viewForm").classList.add("hidden");
      document.getElementById("viewResult").classList.remove("hidden");
      window.scrollTo(0,0);
    });

    // 뒤로 가기
    document.getElementById("backBtn").addEventListener("click", () => {
      document.getElementById("viewResult").classList.add("hidden");
      document.getElementById("viewForm").classList.remove("hidden");
    });

  </script>
</body>
</html>




