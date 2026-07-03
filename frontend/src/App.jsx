import React, { useState } from "react";
import {
    MapContainer,
    TileLayer,
    Polyline,
    Marker,
    Popup,
} from "react-leaflet";
import { jsPDF } from "jspdf";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

const defaultIcon = new L.Icon({
    iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
    iconRetinaUrl:
        "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
    shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
    iconSize: [25, 41],
    iconAnchor: [12, 41],
});

// ... rest of your App component remains exactly the same

export default function App() {
    const [formData, setFormData] = useState({
        current_location: "Los Angeles, CA",
        pickup_location: "Phoenix, AZ",
        dropoff_location: "Dallas, TX",
        current_cycle_used: "12",
    });

    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);

    const handleRouteCalculation = async () => {
        setLoading(true);
        try {
            const response = await fetch(
                "http://127.0.0.1:8000/api/trips/analyze/",
                {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(formData),
                },
            );
            const data = await response.json();
            setResult(data);
        } catch (error) {
            console.error("Error evaluating route:", error);
            alert("Failed to connect to the backend API.");
        } finally {
            setLoading(false);
        }
    };

    const handleDownloadPDF = () => {
        if (!result || !result.logs || result.logs.length === 0) return;
        const doc = new jsPDF({
            orientation: "landscape",
            unit: "px",
            format: [1000, 600],
        });
        result.logs.forEach((base64String, index) => {
            if (index > 0) doc.addPage([1000, 600], "landscape");
            const imgData = `data:image/png;base64,${base64String}`;
            doc.addImage(imgData, "PNG", 0, 0, 1000, 600);
        });
        doc.save("Driver_HOS_Logs.pdf");
    };

    return (
        // True Black background for Apple dark mode
        <div className="min-h-screen bg-black text-white font-sans antialiased p-6 md:p-10 selection:bg-[#0A84FF]/30">
            {/* Header */}
            <header className="max-w-7xl mx-auto mb-10">
                <h1 className="text-4xl md:text-5xl font-bold tracking-tight text-white mb-2">
                    HOS Navigator
                </h1>
                <p className="text-[#8E8E93] text-lg font-medium">
                    Automated ELD Logs & Route Optimization
                </p>
            </header>

            <main className="max-w-7xl mx-auto flex flex-col gap-8">
                {/* TOP ROW: Form & Map locked to the same height using Grid */}
                <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch min-h-125">
                    {/* Trip Details Card */}
                    <div className="lg:col-span-4 bg-[#1C1C1E] rounded-3xl p-8 flex flex-col border border-[#2C2C2E] shadow-2xl">
                        <h2 className="text-[22px] font-semibold mb-6 text-white tracking-tight">
                            Trip Details
                        </h2>

                        <div className="flex flex-col gap-4 grow">
                            {/* Custom Apple-Style Input */}
                            <div>
                                <label className="block text-[13px] font-medium text-[#8E8E93] ml-1 mb-1.5 uppercase tracking-wider">
                                    Current Location
                                </label>
                                <input
                                    type="text"
                                    value={formData.current_location}
                                    onChange={(e) =>
                                        setFormData({
                                            ...formData,
                                            current_location: e.target.value,
                                        })
                                    }
                                    placeholder="e.g. Los Angeles, CA"
                                    className="w-full bg-[#2C2C2E] text-white text-[17px] rounded-[14px] px-4 py-3.5 outline-none focus:ring-[3px] focus:ring-[#0A84FF]/50 border border-transparent focus:border-[#0A84FF] transition-all placeholder-[#636366]"
                                />
                            </div>

                            <div>
                                <label className="block text-[13px] font-medium text-[#8E8E93] ml-1 mb-1.5 uppercase tracking-wider">
                                    Pickup Location
                                </label>
                                <input
                                    type="text"
                                    value={formData.pickup_location}
                                    onChange={(e) =>
                                        setFormData({
                                            ...formData,
                                            pickup_location: e.target.value,
                                        })
                                    }
                                    placeholder="e.g. Phoenix, AZ"
                                    className="w-full bg-[#2C2C2E] text-white text-[17px] rounded-[14px] px-4 py-3.5 outline-none focus:ring-[3px] focus:ring-[#0A84FF]/50 border border-transparent focus:border-[#0A84FF] transition-all placeholder-[#636366]"
                                />
                            </div>

                            <div>
                                <label className="block text-[13px] font-medium text-[#8E8E93] ml-1 mb-1.5 uppercase tracking-wider">
                                    Dropoff Location
                                </label>
                                <input
                                    type="text"
                                    value={formData.dropoff_location}
                                    onChange={(e) =>
                                        setFormData({
                                            ...formData,
                                            dropoff_location: e.target.value,
                                        })
                                    }
                                    placeholder="e.g. Dallas, TX"
                                    className="w-full bg-[#2C2C2E] text-white text-[17px] rounded-[14px] px-4 py-3.5 outline-none focus:ring-[3px] focus:ring-[#0A84FF]/50 border border-transparent focus:border-[#0A84FF] transition-all placeholder-[#636366]"
                                />
                            </div>

                            <div>
                                <label className="block text-[13px] font-medium text-[#8E8E93] ml-1 mb-1.5 uppercase tracking-wider">
                                    Cycle Used (Hrs)
                                </label>
                                <input
                                    type="number"
                                    value={formData.current_cycle_used}
                                    onChange={(e) =>
                                        setFormData({
                                            ...formData,
                                            current_cycle_used: e.target.value,
                                        })
                                    }
                                    placeholder="0"
                                    className="w-full bg-[#2C2C2E] text-white text-[17px] rounded-[14px] px-4 py-3.5 outline-none focus:ring-[3px] focus:ring-[#0A84FF]/50 border border-transparent focus:border-[#0A84FF] transition-all placeholder-[#636366]"
                                />
                            </div>
                        </div>

                        {/* Apple Style Button: Bold, rounded, scales on click */}
                        <button
                            onClick={handleRouteCalculation}
                            disabled={loading}
                            className="mt-8 w-full bg-[#0A84FF] hover:bg-[#007AFF] active:scale-[0.97] transition-all duration-200 text-white font-semibold text-[17px] py-4 rounded-[14px] disabled:opacity-50 flex justify-center items-center gap-2"
                        >
                            {loading ? (
                                <svg
                                    className="animate-spin h-5 w-5 text-white"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                >
                                    <circle
                                        className="opacity-25"
                                        cx="12"
                                        cy="12"
                                        r="10"
                                        stroke="currentColor"
                                        strokeWidth="4"
                                    ></circle>
                                    <path
                                        className="opacity-75"
                                        fill="currentColor"
                                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                                    ></path>
                                </svg>
                            ) : (
                                "Generate Logs & Route"
                            )}
                        </button>
                    </div>

                    {/* Map Card */}
                    <div className="lg:col-span-8 bg-[#1C1C1E] rounded-3xl border border-[#2C2C2E] shadow-2xl overflow-hidden relative">
                        {!result ? (
                            <div className="absolute inset-0 flex flex-col items-center justify-center text-[#8E8E93] z-20 pointer-events-none bg-[#1C1C1E]">
                                <p className="text-[17px] font-medium">
                                    Enter trip details to map route
                                </p>
                            </div>
                        ) : null}

                        <MapContainer
                            center={
                                result?.polyline?.length > 0
                                    ? result.polyline[0]
                                    : [39.8283, -98.5795]
                            }
                            zoom={result ? 5 : 4}
                            scrollWheelZoom={false}
                            style={{
                                height: "100%",
                                width: "100%",
                                backgroundColor: "#1C1C1E",
                            }}
                        >
                            <TileLayer
                                url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
                                attribution="&copy; CartoDB"
                            />

                            {result?.polyline && (
                                <Polyline
                                    positions={result.polyline}
                                    color="#0A84FF"
                                    weight={4}
                                    opacity={0.9}
                                />
                            )}

                            {/* Render the calculated stops (Hotels, Fuel, Rest) */}
                            {result?.stops?.map((stop, idx) => (
                                <Marker
                                    key={idx}
                                    position={[stop.lat, stop.lng]}
                                    icon={defaultIcon}
                                >
                                    <Popup>
                                        <div className="text-gray-900 font-sans">
                                            <strong className="block text-sm mb-1">
                                                {stop.type}
                                            </strong>
                                            <span className="text-xs text-gray-600">
                                                Mile Mark: {stop.mile_mark} mi
                                            </span>
                                        </div>
                                    </Popup>
                                </Marker>
                            ))}
                        </MapContainer>
                    </div>
                </div>

                {/* BOTTOM ROW: Results & Logs */}
                {result && (
                    <div className="bg-[#1C1C1E] rounded-3xl p-8 shadow-2xl border border-[#2C2C2E] animate-fade-in-up">
                        {/* Summary Stats */}
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
                            <div className="bg-[#2C2C2E] rounded-[18px] p-6 flex flex-col items-center justify-center transition-transform hover:scale-[1.02]">
                                <p className="text-[13px] text-[#8E8E93] font-semibold uppercase tracking-wider mb-1">
                                    Total Distance
                                </p>
                                <p className="text-4xl font-bold text-white tracking-tight">
                                    {result.route_summary.total_miles}{" "}
                                    <span className="text-xl text-[#8E8E93] font-medium tracking-normal">
                                        mi
                                    </span>
                                </p>
                            </div>
                            <div className="bg-[#2C2C2E] rounded-[18px] p-6 flex flex-col items-center justify-center transition-transform hover:scale-[1.02]">
                                <p className="text-[13px] text-[#8E8E93] font-semibold uppercase tracking-wider mb-1">
                                    Drive Time
                                </p>
                                <p className="text-4xl font-bold text-white tracking-tight">
                                    {result.route_summary.estimated_hours}{" "}
                                    <span className="text-xl text-[#8E8E93] font-medium tracking-normal">
                                        hrs
                                    </span>
                                </p>
                            </div>
                            <div className="bg-[#2C2C2E] rounded-[18px] p-6 flex flex-col items-center justify-center transition-transform hover:scale-[1.02]">
                                <p className="text-[13px] text-[#8E8E93] font-semibold uppercase tracking-wider mb-1">
                                    Log Sheets
                                </p>
                                <p className="text-4xl font-bold text-[#0A84FF] tracking-tight">
                                    {result.route_summary.stops_count}
                                </p>
                            </div>
                        </div>

                        {/* Logs Display & Download */}
                        <div>
                            <div className="flex justify-between items-center mb-6">
                                <h3 className="text-[22px] font-semibold text-white tracking-tight">
                                    Daily Log Sheets
                                </h3>
                                <button
                                    onClick={handleDownloadPDF}
                                    className="bg-[#2C2C2E] hover:bg-[#3A3A3C] active:scale-95 transition-all text-white font-medium text-[15px] px-5 py-2.5 rounded-full flex items-center gap-2"
                                >
                                    <svg
                                        className="w-4 h-4"
                                        fill="none"
                                        stroke="currentColor"
                                        viewBox="0 0 24 24"
                                    >
                                        <path
                                            strokeLinecap="round"
                                            strokeLinejoin="round"
                                            strokeWidth={2}
                                            d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
                                        />
                                    </svg>
                                    Download PDF
                                </button>
                            </div>

                            <div className="flex gap-6 overflow-x-auto pb-6 snap-x scrollbar-thin scrollbar-thumb-[#48484A] scrollbar-track-transparent">
                                {result.logs.map((logBase64, idx) => (
                                    <div
                                        key={idx}
                                        className="snap-center shrink-0 w-full max-w-3xl bg-white rounded-[18px] p-1 shadow-lg transition-transform duration-300 hover:scale-[1.01]"
                                    >
                                        <div className="bg-[#F2F2F7] text-[#1C1C1E] px-5 py-2.5 rounded-t-[14px] font-semibold text-[15px] border-b border-[#E5E5EA] flex justify-between">
                                            <span>Record of Duty Status</span>
                                            <span className="text-[#8E8E93]">
                                                Day {idx + 1}
                                            </span>
                                        </div>
                                        <img
                                            src={`data:image/png;base64,${logBase64}`}
                                            alt={`Log Sheet Day ${idx + 1}`}
                                            className="w-full rounded-b-[14px] object-contain"
                                        />
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                )}
            </main>
        </div>
    );
}
