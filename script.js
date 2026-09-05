/* =========================================
   MOBILE NAVIGATION
========================================= */

const menuBtn =
    document.getElementById("menuBtn");

const navMenu =
    document.getElementById("navMenu");


if (menuBtn && navMenu) {

    menuBtn.addEventListener("click", () => {

        navMenu.classList.toggle("active");

        const isOpen =
            navMenu.classList.contains("active");

        menuBtn.setAttribute(
            "aria-expanded",
            isOpen
        );

    });


    document
        .querySelectorAll("#navMenu a")
        .forEach(link => {

            link.addEventListener("click", () => {

                navMenu.classList.remove("active");

                menuBtn.setAttribute(
                    "aria-expanded",
                    "false"
                );

            });

        });

}


/* =========================================
   PROJECTS
========================================= */

const projectsContainer =
    document.getElementById(
        "projectsContainer"
    );


async function loadProjects() {

    if (!projectsContainer) {
        return;
    }


    try {

        const response = await fetch(
            "http://127.0.0.1:5000/api/projects"
        );


        if (!response.ok) {

            throw new Error(
                "Unable to load projects"
            );

        }


        const projects =
            await response.json();


        if (!projects.length) {
            return;
        }


        projectsContainer.innerHTML = "";


        projects.forEach(
            (project, index) => {

                const card =
                    document.createElement(
                        "article"
                    );


                card.className =
                    "project-card";


                const number =
                    String(index + 1)
                        .padStart(2, "0");


                card.innerHTML = `

                    <span class="project-number">
                        PROJECT ${number}
                    </span>

                    <h3>
                        ${escapeHTML(project.title)}
                    </h3>

                    <p>
                        ${escapeHTML(project.description)}
                    </p>

                    ${
                        project.link
                        ?
                        `
                        <a
                            class="project-link"
                            href="${escapeAttribute(project.link)}"
                            target="_blank"
                            rel="noopener noreferrer"
                        >
                            View Project →
                        </a>
                        `
                        :
                        ""
                    }

                `;


                projectsContainer.appendChild(card);

            }
        );

    }


    catch (error) {

        console.log(
            "Backend not available:",
            error.message
        );

        /*
         * Static project cards remain visible
         * if the backend is not running.
         */

    }

}


/* =========================================
   CONTACT FORM
========================================= */

const contactForm =
    document.getElementById(
        "contactForm"
    );


const formMessage =
    document.getElementById(
        "formMessage"
    );


if (contactForm) {

    contactForm.addEventListener(
        "submit",
        async (event) => {

            event.preventDefault();


            const name =
                document
                    .getElementById("name")
                    .value
                    .trim();


            const email =
                document
                    .getElementById("email")
                    .value
                    .trim();


            const message =
                document
                    .getElementById("message")
                    .value
                    .trim();


            if (!name || !email || !message) {

                formMessage.textContent =
                    "Please fill in all fields.";

                return;

            }


            try {

                const response =
                    await fetch(
                        "http://127.0.0.1:5000/api/contact",
                        {

                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body:
                                JSON.stringify({
                                    name,
                                    email,
                                    message
                                })

                        }
                    );


                const result =
                    await response.json();


                if (!response.ok) {

                    throw new Error(
                        result.error ||
                        "Unable to send message"
                    );

                }


                formMessage.textContent =
                    "Message sent successfully!";


                contactForm.reset();

            }


            catch (error) {

                console.error(error);

                formMessage.textContent =
                    "Backend is not running. Start Flask and try again.";

            }

        }
    );

}


/* =========================================
   SECURITY HELPERS
========================================= */

function escapeHTML(value) {

    const div =
        document.createElement("div");

    div.textContent =
        String(value ?? "");

    return div.innerHTML;

}


function escapeAttribute(value) {

    return String(value ?? "")
        .replace(/&/g, "&amp;")
        .replace(/"/g, "&quot;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");

}


/* =========================================
   START APPLICATION
========================================= */

loadProjects();