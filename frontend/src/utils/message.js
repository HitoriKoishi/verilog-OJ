import { createVNode, render } from 'vue'
import MessageAlert from '../components/MessageAlert.vue'

const messageTypes = ['success', 'error', 'warning', 'info']

const createMessage = (options) => {
  const container = document.createElement('div')
  
  const vm = createVNode(MessageAlert, {
    ...options,
    onClose: () => {
      render(null, container)
      document.body.removeChild(container)
    }
  })
  
  render(vm, container)
  document.body.appendChild(container)
}

const message = {}

messageTypes.forEach(type => {
  message[type] = (content, duration = 2000) => {
    createMessage({
      type,
      message: content,
      duration
    })
  }
})

export default message