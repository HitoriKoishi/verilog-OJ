import { createVNode, render } from 'vue'
import ConfirmDialog from '../components/ConfirmDialog.vue'

const confirm = (options = {}) => {
    return new Promise((resolve) => {
        const container = document.createElement('div')
        
        const vm = createVNode(ConfirmDialog, {
            ...options,
            onConfirm: () => {
                render(null, container)
                document.body.removeChild(container)
                resolve(true)
            },
            onCancel: () => {
                render(null, container)
                document.body.removeChild(container)
                resolve(false)
            }
        })

        render(vm, container)
        document.body.appendChild(container)
    })
}

export default confirm 