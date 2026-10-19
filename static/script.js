let finalContent = "";

async function generateContent() {
    const topic = document.getElementById("topic").value;
    const language = document.getElementById("language").value;

    if (!topic) {
        alert("Please enter a farming topic!");
        return;
    }

    const btn = document.querySelector(".generate-btn");
    btn.disabled = true;
    btn.innerText = "⏳ Generating...";

    document.getElementById("output-section").style.display = "block";
    document.getElementById("share-section").style.display = "none";
    resetPipeline();

    try {
        await animateStep("bar1", "icon1");
        await animateStep("bar2", "icon2");
        await animateStep("bar3", "icon3");
        await animateStep("bar4", "icon4");
        await animateStep("bar5", "icon5");

        const response = await fetch("/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ topic, language })
        });

        const data = await response.json();

        if (data.success) {
            document.getElementById("out-research").innerText = data.research;
            document.getElementById("out-content").innerText = data.content;
            document.getElementById("out-optimized").innerText = data.optimized;
            document.getElementById("out-approved").innerText = data.approved;
            document.getElementById("out-final").innerText = data.final;

            finalContent = data.final;

            const badge = document.getElementById("status-badge");
            badge.innerText = "Approved ✅";
            badge.classList.add("approved");

            document.getElementById("share-section").style.display = "block";
            showToast("Content Generated Successfully!");

        } else {
            alert("Error: " + data.error);
        }

    } catch (error) {
        alert("Something went wrong! Check if server is running.");
        console.error(error);
    }

    btn.disabled = false;
    btn.innerText = "🚀 Generate Content Pipeline";
}

function resetPipeline() {
    for (let i = 1; i <= 5; i++) {
        const bar = document.getElementById("bar" + i);
        const icon = document.getElementById("icon" + i);
        if (bar) bar.style.width = "0%";
        if (icon) {
            icon.classList.remove("done", "active");
        }
    }
    document.getElementById("out-research").innerText = "Processing...";
    document.getElementById("out-content").innerText = "Processing...";
    document.getElementById("out-optimized").innerText = "Processing...";
    document.getElementById("out-approved").innerText = "Processing...";
    document.getElementById("out-final").innerText = "Processing...";

    const badge = document.getElementById("status-badge");
    badge.innerText = "Processing...";
    badge.classList.remove("approved");
}

function animateStep(barId, iconId) {
    return new Promise((resolve) => {
        const bar = document.getElementById(barId);
        const icon = document.getElementById(iconId);
        if (icon) icon.classList.add("active");
        let width = 0;
        const interval = setInterval(() => {
            width += 5;
            if (bar) bar.style.width = width + "%";
            if (width >= 100) {
                clearInterval(interval);
                if (icon) {
                    icon.classList.remove("active");
                    icon.classList.add("done");
                }
                resolve();
            }
        }, 30);
    });
}

function shareWhatsApp() {
    const text = encodeURIComponent(finalContent);
    window.open(`https://wa.me/?text=${text}`, "_blank");
    showToast("Opening WhatsApp...");
}

function shareSMS() {
    const text = encodeURIComponent(finalContent);
    window.open(`sms:?body=${text}`, "_blank");
    showToast("Opening SMS...");
}

function copyContent() {
    navigator.clipboard.writeText(finalContent).then(() => {
        showToast("Copied to clipboard!");
    });
}

function downloadContent() {
    const blob = new Blob([finalContent], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "kisanvaani_content.txt";
    a.click();
    showToast("Downloaded successfully!");
}

function shareEmail() {
    const subject = encodeURIComponent("KisanVaani Agricultural Content");
    const body = encodeURIComponent(finalContent);
    window.open(`mailto:?subject=${subject}&body=${body}`);
    showToast("Opening Email...");
}

function showQR() {
    const text = encodeURIComponent(finalContent.substring(0, 200));
    const qrUrl = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${text}`;
    document.getElementById("qr-image").src = qrUrl;
    const qrContainer = document.getElementById("qr-container");
    qrContainer.style.display = 
        qrContainer.style.display === "none" ? "block" : "none";
    showToast("QR Code Generated!");
}

function showToast(message) {
    let toast = document.getElementById("toast");
    if (!toast) {
        toast = document.createElement("div");
        toast.id = "toast";
        toast.className = "success-toast";
        document.body.appendChild(toast);
    }
    toast.innerText = message;
    toast.style.display = "block";
    setTimeout(() => {
        toast.style.display = "none";
    }, 3000);
}