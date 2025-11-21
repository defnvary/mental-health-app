import './CrisisAlert.css'

const CrisisAlert = ({ resources }) => {
    return (
        <div className='crisis-alert'>
            <div className='crisis-header'>
                <span className='crisis-icon'>⚠️</span>
                <h3>Crisis Resources Available</h3>
            </div>

            <div className="crisis-resources">
                {resources.map((resource, index) => (
                    <div key={index} className='resource-item'>
                        <div className='resource-info'>
                            <strong>{resource.name}</strong>
                            <span className='resource-available'>{resource.available}</span>
                        </div>
                        <a href={`tel:${resource.number}`} className="call-button">
                            Call {resource.number}
                        </a>
                    </div>
                ))}
            </div>

            <p className='crisis-message'>
                You're not alone. Please reach out to one of these resources.
            </p>
        </div>
    )
}

export default CrisisAlert