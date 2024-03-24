let tags = document.getElementsByClassName('project-tag')

for (let i = 0; i < tags.length; i++) {
    tags[i].addEventListener('click', (e) => {
        let tagID = e.target.dataset.tag //獲取project-tag的data-tag="tag.id"
        let projectID = e.target.dataset.project //獲取project-tag的data-project="project.id"

        // console.log("Tag ID:", tagID)
        // console.log("Project ID:", projectID)

        fetch("http://127.0.0.1:8000/api/remove-tag/", {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 'project': projectID, 'tag': tagID })
        })
            .then(response => response.json())
            .then(data => {
                e.target.remove()
            })
    })
}