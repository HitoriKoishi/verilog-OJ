import { createVNode, render } from 'vue'
import MessageAlert from '../components/MessageAlert.vue'

const messageTypes = ['success', 'error', 'warning', 'info']
const GAP = 16 // 消息之间的间距
let messageQueue = []

const adjustMessagePositions = () => {
    let currentTop = 20
    messageQueue.forEach(item => {
        if (item.container) {
            const element = item.container.firstElementChild
            if (element) {
                // 使用 transform 来设置位置
                const translateY = `${currentTop}px`
                element.style.transform = `translate(-50%, ${translateY})`
                currentTop += element.offsetHeight + GAP
            }
        }
    })
}

const createMessage = (options) => {
    const container = document.createElement('div')
    // 设置容器样式
    container.style.position = 'fixed'
    container.style.top = '0'
    container.style.left = '50%'
    container.style.zIndex = '9999'
    container.style.pointerEvents = 'none'

    const vm = createVNode(MessageAlert, {
        ...options,
        onClose: () => {
            // 添加延迟以完成动画
            setTimeout(() => {
                const index = messageQueue.findIndex(item => item.container === container)
                if (index !== -1) {
                    messageQueue.splice(index, 1)
                    adjustMessagePositions()
                }
                render(null, container)
                document.body.removeChild(container)
            }, 300)
        }
    })

    render(vm, container)
    document.body.appendChild(container)

    messageQueue.push({
        container,
        vm
    })

    // 使用 setTimeout 替代 nextTick
    setTimeout(() => {
        adjustMessagePositions()
    }, 0)
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