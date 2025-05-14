document.addEventListener("DOMContentLoaded", function() {
    let counters = document.querySelectorAll(".number-count");
    let speed = 50; // Animatsiya tezligi (kichikroq son tezroq animatsiya qiladi)

    counters.forEach(counter => {
        let target = +counter.getAttribute("data-count");
        let count = 0;

        let updateCount = setInterval(() => {
            count += Math.ceil(target / speed); // Har bir bosqichda qo‘shiladigan qiymat
            if (count >= target) {
                count = target; // Asl qiymatga yetganda to‘xtatish
                clearInterval(updateCount);
            }
            counter.innerText = count;
        }, 50); // Har 50ms da yangilanadi
    });
});