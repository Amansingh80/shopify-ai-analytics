class PythonAgentService
  AGENT_URL = ENV.fetch('PYTHON_AGENT_URL', 'http://localhost:8000')
  TIMEOUT = 30 # seconds

  def initialize(question)
    @question = question
    @store = question.store
  end

  def process
    start_time = Time.current

    response = connection.post('/api/analyze') do |req|
      req.headers['Content-Type'] = 'application/json'
      req.body = request_payload.to_json
      req.options.timeout = TIMEOUT
    end

    result = JSON.parse(response.body, symbolize_names: true)
    
    {
      answer: result[:answer],
      confidence: result[:confidence],
      query_used: result[:query_used],
      data_points: result[:data_points],
      processing_time_ms: ((Time.current - start_time) * 1000).to_i
    }
  rescue Faraday::TimeoutError
    raise StandardError, 'Python agent timeout - question too complex'
  rescue Faraday::Error => e
    Rails.logger.error("Python agent error: #{e.message}")
    raise StandardError, 'Failed to process question with AI agent'
  end

  private

  def request_payload
    {
      store_id: @store.shopify_domain,
      question: @question.question_text,
      context: {
        access_token: @store.access_token,
        api_version: @store.api_version || '2024-01',
        store_metadata: @store.metadata
      }
    }
  end

  def connection
    @connection ||= Faraday.new(url: AGENT_URL) do |f|
      f.request :retry, {
        max: 2,
        interval: 0.5,
        backoff_factor: 2,
        exceptions: [Faraday::TimeoutError, Faraday::ConnectionFailed]
      }
      f.adapter Faraday.default_adapter
    end
  end
end