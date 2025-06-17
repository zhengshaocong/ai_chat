interface CodeBlock {
  code: string
  language: string
  start: number
  end: number
}

export function parseCodeBlocks(content: string): CodeBlock[] {
  const codeBlocks: CodeBlock[] = []
  const regex = /```(\w+)?\n([\s\S]*?)```/g
  let match

  while ((match = regex.exec(content)) !== null) {
    const language = match[1] || 'plaintext'
    const code = match[2].trim()
    codeBlocks.push({
      code,
      language,
      start: match.index,
      end: match.index + match[0].length
    })
  }

  return codeBlocks
}

export function splitMessageWithCodeBlocks(content: string): (string | CodeBlock)[] {
  const codeBlocks = parseCodeBlocks(content)
  const result: (string | CodeBlock)[] = []
  let lastIndex = 0

  codeBlocks.forEach(block => {
    if (block.start > lastIndex) {
      result.push(content.slice(lastIndex, block.start))
    }
    result.push(block)
    lastIndex = block.end
  })

  if (lastIndex < content.length) {
    result.push(content.slice(lastIndex))
  }

  return result
} 