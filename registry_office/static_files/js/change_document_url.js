const selectedDocumentOptions = document.querySelectorAll(".select-document > button")

const preViewBtn = () => {
    if (selectedDocumentOptions.length === 0) {
        document.querySelector(".preview").style.display = "none"
    }
}

preViewBtn()

const changeDocument = (documentUrl) => {
    const [embed, showDocument] = document.querySelectorAll(".document-url")
    embed.src = documentUrl
    showDocument.href = documentUrl
}

const documentOptions = () => {

    const selectDocument = (e) => {
        const data = e.target
        const url = data.getAttribute('data')
        changeDocument(url)
    }

    selectedDocumentOptions.forEach(b => b.addEventListener('click', selectDocument))
}


documentOptions()