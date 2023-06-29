#import asyncio //굳이 import 하지 않아도 된다고 함. 문제 생기면 할 것.
#aiohttp : asyncio를 기반으로 한 비동기 HTTP 클라이언트/서버 라이브러리
from aiohttp import web
#aiortc: Python으로 작성된 WebRTC 및 ORTC 라이브러리
from aiortc import RTCPeerConnection, RTCSessionDescription, RTCIceCandidate

#web.RouteTableDef()는 aiohttp 서버의 라우팅 테이블을 정의하는 객체를 생성
routes = web.RouteTableDef()

#index 함수는 'WebRTC Server'라는 텍스트를 응답으로 반환
@routes.get('/')
async def index(request):
    return web.Response(text="WebRTC Server")

#'offer 함수는 json을 파싱하여 SDP offer를 생성하고, RTCPeerConnenction 객체를 생성
@routes.post('/offer')
async def offer(request):
    params = await request.json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])
    pc = RTCPeerConnection()
    
    #track의 종류를 출력하도록 설정되어 있음, 여기에는 음성을 텍스트로 변환하고 필터링/요약하는 코드 추가하면 됨!!!
    @pc.on("track")
    def on_track(track):
        print("Receiving %s track" % track.kind)


    #웹RTC 서버는 웹 브라우저와의 연결에 필요한 정보를 얻게 됨
    await pc.setRemoteDescription(offer)
    #'offer'에 대한 'answer' SDP를 생성
    answer = await pc.createAnswer()
    #이 과정이 완료되면, 웹RTC 서버는 생성한 'answer' SDP를 웹 브라우저에게 전송하게 됨. 이를 통해 웹 브라우저와 웹RTC 서버 간의 연결 설정이 완료됨

    #생성된 'answer' SDP를 웹RTC 서버의 'local description'으로 설정
    await pc.setLocalDescription(answer)

    #SDP answer를 JSON 형식으로 응답으로 반환
    return web.json_response({
        "sdp": pc.localDescription.sdp,
        "type": pc.localDescription.type
    })

#web.Application()으로 aiohttp 애플리케이션을 생성하고, 앞서 정의한 라우트를 추가한 후 애플리케이션을 실행
app = web.Application()
app.router.add_routes(routes)

web.run_app(app)
