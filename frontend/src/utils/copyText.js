

export default function copyText(text){
    const input = document.createElement("input");
    document.body.appendChild(input);

    input.value = text
    input.select()

    document.execCommand("copy", false)
    input.remove()

}