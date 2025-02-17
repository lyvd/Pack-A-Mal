async function load() {
    try {
        let currentUrl = window.location.href;
        currentUrl = currentUrl.split('/package-analysis')[0] + '/package-analysis';
        let response = await fetch( `${currentUrl}/get_wolfis_packages`);
        let data = await response.json();
        return data.packages;
    } catch (error) {
        console.error('Error:', error);
        return [];
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("package_name");
    const suggestions = document.getElementById("suggestions");

    load().then(package_names => {
        input.addEventListener("input", function() {
            const value = this.value.toLowerCase();
            suggestions.innerHTML = "";

            if (value) {
                const filteredPackages = package_names.filter(package_name => package_name.toLowerCase().includes(value));

                if (filteredPackages.length > 0) {
                    suggestions.style.display = "block";
                    filteredPackages.forEach(package_name => {
                        const div = document.createElement("div");
                        div.textContent = package_name;
                        div.addEventListener("click", function() {
                            input.value = package_name;
                            suggestions.style.display = "none";
                        });
                        suggestions.appendChild(div);
                    });
                } else {
                    suggestions.style.display = "none";
                }
            } else {
                suggestions.style.display = "none";
            }
        });
    });

    document.addEventListener("click", (e) => {
        if (!document.querySelector("#package_name").contains(e.target) && !suggestions.contains(e.target)) {
            suggestions.style.display = "none";
        }
    });
});    


